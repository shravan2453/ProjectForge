from typing import Annotated
from typing_extensions import TypedDict
import os
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory  import MemorySaver


load_dotenv()  # Load environment variables from .env file if it exists
api_key = os.getenv("gemini_api_key")

'''
tavily_api_key = os.getenv("TAVILY_API_KEY")


#INITIALIZING TAVILY SEARCH TOOL

tool = TavilySearch(max_results=2)  # Initialize the Tavily search tool with a maximum of 2 results per query
tools = [tool]  # Create a list of tools to be used by the LLM
tool.invoke("What is a tool in LangGraph?")  # Example tool invocation to test functionality
'''


#INTIALIZING MEMORY
memory = MemorySaver()


#INITIALIZING CHATBOT

from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = api_key

llm = init_chat_model("google_genai:gemini-2.0-flash")


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

#llm_with_tools = llm.bind_tools(tools)


#INCORPORATING CHATBOT INTO A NODE

def chatbot(state: State):
    return {"messages" : [llm.invoke(state["messages"])]}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)


#CREATE FUNCTION TO HANDLE TOOL CALLS
'''
import json
from langchain_core.messages import ToolMessage

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name =  {tool.name: tool for tool in tools}
    
    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No messages found in inputs")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}



tool_node = ToolNode(tools=[tool])
#graph_builder.add_node("tools", tool_node)

from langgraph.graph import END


def route_tools(state: State):
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

# The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
# It defaults to the identity function, but if you
# want to use a node named something else apart from "tools",
# You can update the value of the dictionary to something else
# e.g., "tools": "my_tools"

graph_builder.add_conditional_edges("chatbot", tools_condition, {"tools": "tools", END: END})
'''

#graph_builder.add_conditional_edges("chatbot",tools_condition)

#ADDING THE ENTRY POINT

#graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile(checkpointer=memory)




#VISUALIZE THE GRAPH
'''
from IPython.display import Image, display
    

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass
'''

from langchain_core.messages import AIMessage

def stream_graph_updates(user_input: str, thread_id="1"):
    config = {"configurable": {"thread_id": thread_id}}
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"):
        last_msg = event["messages"][-1]
        if isinstance(last_msg, AIMessage):                   # print only assistant turns
            print("Assistant:", last_msg.content)


while True:
    thread_id = 1
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input, thread_id)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break