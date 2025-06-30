"""
backend.py  ―  FastAPI + LangGraph server for “Project-Idea” chatbot

Run locally:
    $ pip install fastapi uvicorn python-dotenv langchain langgraph langchain-tavily
    $ python backend.py         # reload=True is enabled below

POST /simple-chat
Request : {
    "thread_id": string | null,   # optional, FE stores it after 1st reply
    "messages" : [ { "role": "...", "content": "..." }, ... ]   # history slice (user+assistant)
}
Response: {
    "assistant_message": string,  # bot’s reply for this turn
    "final_idea"      : string | null,   # filled once router → finalize
    "thread_id"       : string          # echo so FE can persist
}
"""

# ────────────────────────── 1.  Imports & setup ──────────────────────────
import os, uuid
from typing import Annotated, List, TypedDict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_tavily import TavilySearch     # ← keep if you add tools later
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# ────────────────────────── 2.  Env & LLM ────────────────────────────
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini_api_key")       # Gemini key (Google GenAI)
llm = init_chat_model("google_genai:gemini-2.0-flash")

# ────────────────────────── 3.  State schema ─────────────────────────
def add_lists(old: List[str], new: List[str]) -> List[str]:
    return old + new

class State(TypedDict):
    messages:        Annotated[list, add_messages]
    rejected_ideas:  Annotated[List[str], add_lists]
    preferences:     Annotated[List[str], add_lists]
    accepted_idea:   str | None

# ────────────────────────── 4.  Node definitions ─────────────────────
def chatbot(state: State):
    system = (
        "You are an idea-generation bot.\n"
        f"Previously rejected ideas: {state['rejected_ideas'][-5:]}\n"
        f"User preferences: {state['preferences'][-5:]}\n"
        "Return ONE new project idea (or ask up to 2 clarifying questions)."
    )
    prompt = [{"role": "system", "content": system}] + state["messages"]
    return {"messages": [llm.invoke(prompt)]}

def _last_ai_message(state: State) -> str:
    for m in reversed(state["messages"]):
        if isinstance(m, AIMessage):
            return m.content
    return ""

def classify_intent(text: str) -> str:
    instruction = (
        "Classify the user's message into one word ONLY—"
        "ACCEPT, REJECT, PREFERENCE, OTHER.\n"
        "Only say ACCEPT if the user clearly approves the ENTIRE idea.\n\n"
        f"User: {text}"
    )
    return llm.invoke(instruction).content.strip().upper()

def router_node(_: State) -> dict:
    return {}          # no-op; required update dict

def route_decision(state: State) -> str:
    intent = classify_intent(state["messages"][-1].content)
    if intent == "ACCEPT":
        return "finalize"
    if intent == "REJECT":
        idea = _last_ai_message(state)
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
    raw = _last_ai_message(state)            # most recent idea from assistant
    formatted = llm.invoke(
        TEMPLATE +
        "\n\n---\nGiven the text below, fill in the brackets ONLY. ONLY Fill in the template and bold the headers."
        "Dont make the description of the overview too long, make it easy to read for the user, but also "
        "make the overview detailed enough for a student to follow.\n\n" +
        raw
    ).content
    state["accepted_idea"] = formatted
    return {"messages": [AIMessage(content=formatted)]}

# ────────────────────────── 5.  Build the graph ──────────────────────
graph_builder = StateGraph(State)
graph_builder.add_node("router", router_node)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("finalize", finalize)

graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges(
    "router", route_decision,
    {"chatbot": "chatbot", "finalize": "finalize", END: END}
)
graph_builder.add_edge("chatbot", END)
graph_builder.add_edge("finalize", END)

graph = graph_builder.compile(checkpointer=MemorySaver())

# ────────────────────────── 6.  FastAPI layer ────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # ⬅️ tighten in production
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    thread_id: str | None = None
    messages:  list
    rejected_ideas: List[str] | None = None

class ChatResponse(BaseModel):
    assistant_message: str
    final_idea: str | None
    thread_id: str
    rejected_ideas: List[str]

@app.post("/simple-chat", response_model=ChatResponse)
def simple_chat(req: ChatRequest):
    # pick / reuse thread id
    thread_id = req.thread_id or uuid.uuid4().hex

    # last user message = newest with role 'user'
    last_user = next(m for m in reversed(req.messages) if m["role"] == "user")

    init_state = {
        "messages":       [last_user],
        "rejected_ideas": [],
        "preferences":    req.preferences    or [],
    }
    cfg = {"configurable": {"thread_id": thread_id}}

    final_state = None
    for final_state in graph.stream(init_state, cfg, stream_mode="values"):
        pass

    return ChatResponse(
        assistant_message = final_state["messages"][-1].content,
        final_idea        = final_state.get("accepted_idea"),
        thread_id         = thread_id,
        preferences       = final_state["preferences"],
    )

# ────────────────────────── 7.  Dev server entrypoint ───────────────
# Run with:  uvicorn chatbot_backend:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("chatbot_backend:app", host="0.0.0.0", port=8000, reload=True)
