from typing import Annotated, List
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


#INTIALIZING MEMORY
memory = MemorySaver()


#INITIALIZING CHATBOT

from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = api_key

llm = init_chat_model("google_genai:gemini-2.0-flash")

def add_lists(old: List[str], new: List[str]) -> List[str]:
    """merge rule ─ append instead of overwrite"""
    return old + new

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    rejected_ideas: Annotated[List[str], add_lists]
    preferences: Annotated[List[str], add_lists]
    accepted_idea: str | None

graph_builder = StateGraph(State)

#llm_with_tools = llm.bind_tools(tools)


#INCORPORATING CHATBOT INTO A NODE

def chatbot(state: State):
    system = (
        "You are an idea-generation bot. "
        f"Previously rejected ideas: {state['rejected_ideas'][-5:]}\n"
        f"User preferences: {state['preferences'][-5:]}\n"
        "Generate ONE new project idea unless the user says something else. " \
        "Ask clarifying questions to get a better sense of the user requires."
        "ONLY PROVIDE ONE IDEA AT A TIME, OR MAKE SURE TO ASK 1-2 CLARIFYING QUESTIONS WITH EACH ITERATION TO HELP WITH COMING UP WITH A GOOD IDEA."
    )
    prompt = [{"role": "system", "content": system}] + state["messages"]
    return {"messages": [llm.invoke(prompt)]}

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.


#FEEDBACK COLLECTOR NODE

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END 

def _last_ai_message(state: State) -> str:
    """Return content of newest AIMessage in history ('' if none)."""
    for m in reversed(state["messages"]):
        if isinstance(m, AIMessage):
            return m.content
    return ""

def classify_intent(user_text: str) -> str:
    """
    Return one of: ACCEPT, REJECT, PREFERENCE, OTHER
    """
    prompt = (
        "Classify the user's message into one word (ACCEPT, REJECT, "
        "PREFERENCE, OTHER). Only say ACCEPT if you are confident that"
        "the user is approving THE WHOLE IDEA. MAKE SURE THAT YOU HAVE" \
        "IF YOU FEEL YOU DON'T HAVE ENOUGH INFO ON THE IDEA, THEN" \
        "DONT RETURN ACCEPT."
        "Most importantly: Only output the word.\n\n"
        f"User: {user_text}"
    )
    return llm.invoke(prompt).content.strip().upper()


def router_node(_: State) -> dict:      
    return {}                             

def route_decision(state: State) -> str:   
    last = state["messages"][-1]
    intent = classify_intent(last.content)

    if intent == "ACCEPT":
        return "finalize"
    if intent == "REJECT":
        idea = _last_ai_message(state)
        if idea:
            state["rejected_ideas"].append(idea)
        return "chatbot"
    if intent == "PREFERENCE":
        state["preferences"].append(last.content)
        return "chatbot"
    return "chatbot"





# FINALIZE NODE - ACCEPTING FINAL IDEA AND STORE
TEMPLATE = (
    "Project Name: {name}\n"
    "Project Overview: {overview}\n"
    "Project Difficulty: {difficulty}\n"
    "Project Timeline: {timeline}"
)

def finalize(state: State):
    raw = state["messages"][-2].content        # accepted idea = previous AI turn
    formatted = llm.invoke(
        TEMPLATE + "\n\n---\nGiven the text below, fill in the brackets ONLY:\n\n. Make sure the description is very detailed and covers all"
        "bases for a student to use in detail and pass on." + raw
    ).content
    state["accepted_idea"] = formatted
    return {"messages": [AIMessage(content=formatted)]}

#ADDING THE ENTRY POINTS

graph_builder.add_node("router", router_node)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("finalize", finalize)

graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges(
    "router",
    route_decision,              
    {"finalize": "finalize",
     "chatbot":  "chatbot",
     END: END}
)
graph_builder.add_edge("chatbot", END)          
graph_builder.add_edge("finalize", END)


graph = graph_builder.compile(checkpointer=memory)

from langchain_core.messages import AIMessage

def stream_graph_updates(user_input: str, thread_id="1"):
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "rejected_ideas": ['Quarterback Football Injury rate'],
       "preferences": [
           '24 Hour Hackathon',
           'Focus on Full Stack',
           'Sports Analytics'
       ],
    }
    for event in graph.stream(initial_state, config, stream_mode="values"):
        last_msg = event["messages"][-1]
        if isinstance(last_msg, AIMessage):                   # print only assistant turns
            print("Assistant:", last_msg.content)


print("Hello there! Lets find a great idea for you!")
while True:
    thread_id = 1
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input, thread_id)