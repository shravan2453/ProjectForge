# project_idea_graph.py  – builds & exports `graph`
import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini_api_key")
llm = init_chat_model("google_genai:gemini-2.0-flash")

def add_lists(old: List[str], new: List[str]) -> List[str]:
    return old + new

class State(TypedDict):
    messages:        Annotated[list, add_messages]
    rejected_ideas:  Annotated[List[str], add_lists]
    preferences:     Annotated[List[str], add_lists]
    accepted_idea:   str | None

# ---------- nodes ----------
def chatbot(state: State):
    system = (
        "You are an idea-generation bot.\n"
        f"Previously rejected ideas: {state['rejected_ideas'][-5:]}\n"
        f"User preferences: {state['preferences'][-5:]}\n"
        "Return ONE new project idea or ask clarifying questions."
    )
    prompt = [{"role": "system", "content": system}] + state["messages"]
    return {"messages": [llm.invoke(prompt)]}

def _last_ai(state: State) -> str:
    for m in reversed(state["messages"]):
        if isinstance(m, AIMessage):
            return m.content
    return ""

def classify_intent(text: str) -> str:
    ask = (
        "Classify into ACCEPT, REJECT, PREFERENCE, OTHER. "
        "Only ACCEPT if the user clearly approves the *whole* idea.\n\n"
        f"User: {text}"
    )
    return llm.invoke(ask).content.strip().upper()

def router_node(_: State) -> dict:       # dummy node
    return {}

def route_decision(state: State) -> str:
    intent = classify_intent(state["messages"][-1].content)
    if intent == "ACCEPT":
        return "finalize"
    if intent == "REJECT":
        idea = _last_ai(state)
        if idea:
            state["rejected_ideas"].append(idea)
        return "chatbot"
    if intent == "PREFERENCE":
        state["preferences"].append(state["messages"][-1].content)
        return "chatbot"
    return "chatbot"

TEMPLATE = (
    "Project Name: {name}\n"
    "Project Overview: {overview}\n"
    "Project Difficulty: {difficulty}\n"
    "Project Timeline: {timeline}"
)

def finalize(state: State):
    raw = _last_ai(state)
    state["accepted_idea"] = llm.invoke(
        TEMPLATE + "\n\n---\nFill the brackets for the idea below:\n\n" + raw
    ).content
    return {"messages": [AIMessage(content=state["accepted_idea"])]}

# ---------- graph ----------
gb = StateGraph(State)
gb.add_node("router", router_node)
gb.add_node("chatbot", chatbot)
gb.add_node("finalize", finalize)
gb.add_edge(START, "router")
gb.add_conditional_edges("router", route_decision,
                         {"chatbot": "chatbot", "finalize": "finalize", END: END})
gb.add_edge("chatbot", END)
gb.add_edge("finalize", END)

graph = gb.compile(checkpointer=MemorySaver())   # ← exported symbol
