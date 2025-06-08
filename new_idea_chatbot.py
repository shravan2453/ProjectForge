# ✅ chatbot_langgraph.py (fully fixed with RunnableLambda)
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import List, Dict, Optional, Annotated
import google.generativeai as genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langgraph.graph.message import add_messages

load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))

model = genai.GenerativeModel("gemini-2.0-flash")

class ProjectChatState(BaseModel):
    messages: Annotated[List[Dict[str, str]], add_messages] = []
    accepted: bool = False
    final_idea: Optional[str] = None

def build_initial_context(form_inputs: Dict[str, str], rejected_ideas: List[str]) -> str:
    context = f"""
        You are helping a student come up with a creative and practical project idea.

        Here is what they said they are looking for:
        - Project Type: {form_inputs.get('project_type', 'N/A')}
        - Interest Domain: {form_inputs.get('project_interest', 'N/A')}
        - Technical Skills: {form_inputs.get('project_technical', 'N/A')}
        - Ideation Status: {form_inputs.get('project_potential', 'N/A')}
        - Additional Notes: {form_inputs.get('project_additional', 'None')}

        They already rejected the following project ideas:
    """
    if rejected_ideas:
        for idea in rejected_ideas:
            context += f"\n- {idea}"
    else:
        context += "\n- (None yet)"

    context += """

        Please do NOT suggest any of the rejected ideas again. Start by asking a clarifying question or suggesting a new idea that aligns better with the preferences.
        """
    return context.strip()

def chat_node(state: ProjectChatState) -> ProjectChatState:
    gemini_messages = []
    for msg in state.messages:
        if msg["role"] == "system":
            continue  # skip system/context messages
        role = "user" if msg["role"] == "user" else "model"  # map 'assistant' to 'model'
        gemini_messages.append({"role": role, "parts": [msg["content"]]})

    # Only send if there is at least one user message
    if not gemini_messages or gemini_messages[-1]["role"] != "user":
        return state

    chat = model.start_chat(history=gemini_messages[:-1])  # all but last user message
    response = chat.send_message(gemini_messages[-1]["parts"][0])  # last user message
    state.messages.append({"role": "assistant", "content": response.text.strip()})
    return state

def evaluate_node(state: ProjectChatState) -> str:
    last_input = state.messages[-1]["content"]

    prompt = f"""
    You're evaluating whether this student ACCEPTED a project idea. Return exactly one word: "accepted" or "continue".
    
    Message:
    "{last_input}"
    """
    response = model.generate_content(prompt).text.strip().lower()
    if response not in ["accepted", "continue"]:
        return "continue"
    if response == "accepted":
        state.accepted = True
    return response

def summarize_node(state: ProjectChatState) -> ProjectChatState:
    convo = "\n".join([f'{m["role"].capitalize()}: {m["content"]}' for m in state.messages])
    prompt = f"""
    You are an extremely skilled idea generator, that can come up with extremely creative and applicable ideas for 
    projects for students/users that want to create projects either by themselves or in a group. These ideas may be fully thought out or not thought out at all. Your job is to help them develop the idea into something concrete and adheres to their wishes, no matter how crazy the idea sounds. Specifically, you will take five inputs, and use the responses of the inputs to give the user a set of 5-10 concrete, creative, and applicable project ideas.
    
    Summarize it in the following format:

    - Project Name:
    - Project Overview:
    - Project Difficulty (novice / intermediate / advanced):
    - Project Timeline (approximate hours/week and total weeks it might take):

    Conversation:
    {convo}
    """
    response = model.generate_content(prompt)
    state.final_idea = response.text.strip()
    return state

def get_chat_graph():
    builder = StateGraph(ProjectChatState)
    builder.add_node("chat", RunnableLambda(chat_node))
    builder.add_node("evaluate", RunnableLambda(evaluate_node))
    builder.add_node("summarize", RunnableLambda(summarize_node))
    builder.set_entry_point("chat")
    builder.add_edge("chat", "evaluate")
    
    # Define the conditional routing function
    def route_evaluation(state: ProjectChatState) -> str:
        return "accepted" if state.accepted else "continue"
    
    builder.add_conditional_edges(
        "evaluate",
        RunnableLambda(route_evaluation),
        {
            "accepted": "summarize",
            "continue": "chat"
        }
    )
    builder.add_edge("summarize", END)
    return builder.compile()


