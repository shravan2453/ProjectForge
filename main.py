from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict

from new_idea_chatbot import get_chat_graph, ProjectChatState, build_initial_context

load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))
model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI()  # ✅ ONLY ONCE

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- /generate route ---
class InputData(BaseModel):
    project_type: str
    project_interest: str
    project_technical: str
    project_potential: str
    project_additional: str

@app.post("/generate")
def generate_ideas(data: InputData):
    prompt = f"""
    You are an extremely skilled idea generator, that can come up with extremely creative and applicable ideas for 
    projects for students/users that want to create projects either by themselves or in a group. These ideas may be fully thought out or 
    not thought out at all. Your job is to help them develop the idea into something concrete and adheres to their wishes, no matter 
    how crazy the idea sounds. Specifically, you will take five inputs, and use the responses of the inputs to give the user a set of 5-10 concrete, creative, and applicable project ideas.
    
    Here are the inputs:
    - Project Type: {data.project_type}
    - Interest Domain: {data.project_interest}
    - Technical Skills: {data.project_technical}
    - Ideation Status: {data.project_potential}
    - Additional Notes: {data.project_additional}

    Please provide 5-10 project ideas. For each idea, use this exact format:

    Project Name: [Name of the project]
    Project Overview: [Brief description of what the project does]
    Project Difficulty: [novice/intermediate/advanced]
    Project Timeline: [hours per week and total weeks]

    Make sure each idea is separated by a blank line and follows this exact format.
    """

    response = model.generate_content(prompt)
    raw_output = response.text.strip()

    ideas = []
    current_idea = []
    for line in raw_output.split('\n'):
        if line.strip():
            current_idea.append(line.strip())
        elif current_idea:
            ideas.append('\n'.join(current_idea))
            current_idea = []
    if current_idea:
        ideas.append('\n'.join(current_idea))

    return {"ideas": ideas}

# --- /chat route ---
class MessageInput(BaseModel):
    user_message: str
    previous_messages: List[Dict[str, str]]
    form_inputs: Dict[str, str]
    rejected_ideas: List[str]

def normalize_message(msg):
    if isinstance(msg, dict):
        return msg
    return {
        "role": getattr(msg, "type", "assistant"),
        "content": getattr(msg, "content", "")
    }

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_message = body.get("user_message")
        previous_messages = body.get("previous_messages", [])
        form_inputs = body.get("form_inputs", {})
        rejected_ideas = body.get("rejected_ideas", [])

        cleaned_messages = [normalize_message(m) for m in previous_messages]
        cleaned_messages.append({"role": "user", "content": user_message})

        chat_graph = get_chat_graph()
        state = {
            "messages": cleaned_messages,
            "form_inputs": form_inputs,
            "rejected_ideas": rejected_ideas
        }

        for step in chat_graph.stream(state):
            state.update(step)

        return JSONResponse(content={
            "messages": state.get("messages", []),
            "accepted": state.get("accepted", False),
            "final_idea": state.get("final_idea", None)
        })

    except Exception as e:
        print("🔥 Chat endpoint error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

from fastapi import Request
import google.generativeai as genai
from fastapi.responses import JSONResponse

prompt_intro = """
You are an extremely skilled idea generator, that can come up with extremely creative and applicable ideas for 
projects for students/users that want to create projects either by themselves or in a group. These ideas may be fully thought out or 
not thought out at all. Your job is to help them develop the idea into something concrete and adheres to their wishes, no matter 
how crazy the idea sounds. You need to work with the user until they agree with your ideas and what you want to provide them with.
Most importantly, keep asking clarifying questions until you feel very confident in giving 1-2 good ideas to the user that reflect
their preferences. I would say aim for asking 5-6 clarifying questions TOTAL to the user related to their poject
prior to giving them a final project idea in the output formatted below. Ask the clarifying questions
ONE AT A TIME, rather than just prompting the user with many questions at once. This is VERY important! 
Once they say they are good with the idea, saying something similar to "yes" or "i like this idea" or "ok" or "sure", end with providing them a concrete output that is formatted as such:

Use this exact format:

Project Name: [Name of the project]  
Project Overview: [Brief description of what the project does]  
Project Difficulty: [novice/intermediate/advanced]  
Project Timeline: [hours per week and total weeks the project will take]  
"""

@app.post("/simple-chat")
async def simple_chat(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages", [])

        # Convert to Gemini-compatible chat messages
        chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in messages]

        model = genai.GenerativeModel("gemini-2.0-flash")
        convo = model.start_chat(history=chat_history)
        response = convo.send_message(prompt_intro)

        reply = response.text.strip()

        final_idea = None
        if reply.startswith("Project Name:"):
            final_idea = reply

        return JSONResponse(content={
            "assistant_message": reply,
            "final_idea": final_idea
        })

    except Exception as e:
        print("🔥 simple-chat error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

