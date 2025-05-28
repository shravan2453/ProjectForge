import os
import getpass
import json
# Ensure you have the necessary packages installed:

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import ToolMessage, AIMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver 



load_dotenv()  # Load environment variables from .env file if it exists

openai_api_key = os.getenv("OPENAI_API_KEY")  # Use the OpenAI API key
tavily_api_key = os.getenv("TAVILY_API_KEY")




# This code is an example of how to use LangGraph to create a simple chatbot that interacts with a user

memory = MemorySaver() # Initialize a memory saver to store the state of the graph across runs 
# chage this to connect to database in real application


# Here I create the schema for the graph, essentially defining the structure of the state that will be used in the graph and passed through all nodes.
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages] # add_messages is a reducer function that appends messages to the list, ensuring we do not overwrite previous messages


graph_builder = StateGraph(State) # Create a graph builder that will help build the state graph

tool = TavilySearch(max_results=2) # Initialize the Tavily search tool with a maximum of 2 results per query
tools = [tool] # Create a list of tools to be used by the LLM

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)
llm_with_tools = llm.bind_tools(tools)

def chatbot(state:State): # chatbot incorporated into a single node 
    return {"messages": [llm_with_tools.invoke(state["messages"])]}



graph_builder.add_node("chatbot", chatbot) # Add a node to the graph that uses the chatbot function

graph_builder.add_edge(START, "chatbot") # Connect the START node to the chatbot node



class BasicToolNode: # node that handles tool calls
    def __init__(self, tools:list) -> None:
        """
        Initializes the object with a list of tools.

        Args:
            tools (list): A list of tool objects. Each tool must have a 'name' attribute.

        Attributes:
            tools_by_name (dict): A dictionary mapping tool names to tool objects for quick lookup.
        """
        self.tools_by_name = {tool.name: tool for tool in tools}
    
    def __call__(self, inputs: dict):
        """
        Processes input messages by invoking corresponding tools based on tool calls found in the latest message.

        Args:
            inputs (dict): A dictionary containing a "messages" key with a list of message objects. Each message may contain tool calls.

        Returns:
            dict: A dictionary with a "messages" key containing a list of ToolMessage objects, each representing the result of a tool invocation.

        Raises:
            ValueError: If no messages are found in the input.
        """
        if messages := inputs.get("messages", []):
            message = messages[-1] # set message to the last message in the list
        else:
            raise ValueError("No message found in input")
        TMResponses = []
        for tool_call in message.tool_calls: # Iterate through tool calls in the message
            tool_result = self.tools_by_name[tool_call["name"]].invoke( # tool
                tool_call["args"]   # Invoke the tool with the arguments provided in the tool call
            )
            TMResponses.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": TMResponses} # Return a dictionary with the tool responses as the values



tool_node = BasicToolNode(tools=[tool]) # Create a BasicToolNode instance with the list of tools
graph_builder.add_node("tools", tool_node) # Add the tool node to the graph builder

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
config = {"configurable": {"thread_id": "1"}}
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, 
                              config=config, 
                              stream_mode="values"
                            
                              ):
        for value in event.values():
            if value and isinstance(value[-1], AIMessage):
                print("Assistant:", value[-1].content)
            

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break