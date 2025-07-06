# main.py  ---------------------------------------------------------------
from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import os, uuid
import google.generativeai as genai
from dotenv import load_dotenv

# ───── Env & Gemini model ───────────────────────────────────────────────
load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# ───── FastAPI instance & CORS ──────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # <- loosen later for prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════════════════
# 1)  GENERATE IDEAS (Gemini, no chat / memory)
# ════════════════════════════════════════════════════════════════════════
class InputData(BaseModel):
    project_type: str
    project_interest: str
    project_technical: str
    project_potential: str
    project_additional: str
    uploaded_document: Optional[dict] = None

@app.post("/generate")
def generate_ideas(data: InputData):
    # Build the prompt with document content if available
    document_context = ""
    if data.uploaded_document and data.uploaded_document.get('content'):
        document_context = f"""
        
Additional Guidelines/Instructions from uploaded document:
{data.uploaded_document['content']}

Please consider these guidelines when generating project ideas.
"""
    
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
    - Additional Notes: {data.project_additional}{document_context}

    Please provide 5-10 project ideas. For each idea, use this exact format:

    Project Name: [Name of the project]
    Project Overview: [Brief description of what the project does]
    Project Skills: [What skills are required to complete the project(technical skills, no-code, etc.)]
    Project Difficulty: [novice/intermediate/advanced]
    Project Timeline: [hours per week and total weeks]

    Make sure each idea is separated by a blank line and follows this exact format.
    """
    raw = gemini_model.generate_content(prompt).text.strip()

    # Split into individual ideas (same logic as before)
    ideas, current = [], []
    for line in raw.splitlines():
        if line.strip():
            current.append(line.strip())
        elif current:
            ideas.append("\n".join(current)); current = []
    if current:
        ideas.append("\n".join(current))
    return {"ideas": ideas}

# ════════════════════════════════════════════════════════════════════════
# 2)  SIMPLE GEMINI CHAT  (unchanged)
# ════════════════════════════════════════════════════════════════════════
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
Project Skills: [What skills are required to complete the project(technical skills, no-code, etc.)]
Project Difficulty: [novice/intermediate/advanced]  
Project Timeline: [hours per week and total weeks the project will take]  
"""

@app.post("/simple-chat")
async def simple_chat(request: Request):
    try:
        body     = await request.json()
        messages = body.get("messages", [])

        chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in messages]
        convo  = gemini_model.start_chat(history=chat_history)
        reply  = convo.send_message(prompt_intro).text.strip()

        return JSONResponse(content={
            "assistant_message": reply,
            "final_idea": reply if reply.startswith("Project Name:") else None
        })
    except Exception as e:
        print("🔥 simple-chat error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

# ════════════════════════════════════════════════════════════════════════
# 3)  LANGGRAPH CHAT  (/lg-chat)
# ════════════════════════════════════════════════════════════════════════
from chatbot_backend import graph   # <-- make sure this file exports `graph`

class LGRequest(BaseModel):
    thread_id: Optional[str] = None
    messages: List[Dict[str, str]]
    preferences: List[str] = []

class LGResponse(BaseModel):
    assistant_message: str
    final_idea: Optional[str]
    thread_id: str
    is_final: bool

@app.post("/lg-chat", response_model=LGResponse)
def lg_chat(data: LGRequest = Body(...)):
    thread_id = data.thread_id or uuid.uuid4().hex
    last_user = next(m for m in reversed(data.messages) if m["role"] == "user")

    init_state = {
        "messages":       [last_user],
        "rejected_ideas": [],
        "preferences":    data.preferences or [],
    }
    cfg = {"configurable": {"thread_id": thread_id}}

    # run exactly one LangGraph pass
    final_state = None
    for final_state in graph.stream(init_state, cfg, stream_mode="values"):
        pass

    return LGResponse(
        assistant_message = final_state["messages"][-1].content,
        final_idea        = final_state.get("accepted_idea"),
        thread_id         = thread_id,
        is_final          = final_state.get("accepted_idea") is not None,
    )