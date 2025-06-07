from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from new_idea_chatbot import get_chat_graph, ProjectChatState, build_initial_context
from fastapi.responses import JSONResponse

load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))
model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    # Split the output into individual ideas
    ideas = []
    current_idea = []
    
    for line in raw_output.split('\n'):
        if line.strip():
            current_idea.append(line.strip())
        elif current_idea:
            ideas.append('\n'.join(current_idea))
            current_idea = []
    
    if current_idea:  # Don't forget the last idea
        ideas.append('\n'.join(current_idea))
    
    return {"ideas": ideas}

# Setup LangGraph Chatbot
graph = get_chat_graph()

class MessageInput(BaseModel):
    user_message: str
    previous_messages: List[Dict[str, str]]
    form_inputs: Dict[str, str]
    rejected_ideas: List[str]

@app.post("/chat")
def chat_with_gemini(data: MessageInput):
    try:
        messages = list(data.previous_messages)
        if not messages:
            # Add a system/context message for the model
            context_message = build_initial_context(data.form_inputs, data.rejected_ideas)
            messages.append({"role": "system", "content": context_message})
            # Add the greeting as the first assistant message
            messages.append({"role": "assistant", "content": "Hello there lets find a great idea for you!"})
        messages.append({"role": "user", "content": data.user_message})
        state = ProjectChatState(messages=messages)
        result = graph.invoke(state)

        return {
            "final_idea": result.final_idea,
            "messages": result.messages,
            "accepted": result.accepted
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
