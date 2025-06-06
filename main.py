from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Configure Gemini API key
gemini_key = os.getenv("gemini_api_key") 
genai.configure(api_key=gemini_key)  # Replace with your key

# Define app
app = FastAPI()

# Allow frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input structure
class InputData(BaseModel):
    project_type: str
    project_interest: str
    project_technical: str
    project_potential: str
    project_additional: str

@app.post("/generate")
def generate_ideas(data: InputData):
    # Construct prompt using form data
    prompt = f"""You are an extremely skilled idea generator, that can come up with extremely creative and applicable ideas for 
    projects for students/users that want to create projects either by themselves or in a group. These ideas may be fully thought out or 
    not thought out at all. Your job is to help them develop the idea into something concrete and adheres to their wishes, no matter 
    how crazy the idea sounds. Specifically, you will take five inputs, and use the responses of the inputs to give the user a set of 5-10 concrete, creative, and applicable project ideas.
        
        The first input that you will be provided with is information of what the project is for. The purpose oof this input is to give
        a sense of the context of the project. For example, the project could be for a potential startup, it could be for a
        hackathon, or it could be something like a personal website. Use this input to understand exactly what kind of projects you
        can give to the user. 
        This is the first input that you will use: {data.project_type}
        
        The second input that you will be provided with is the sort of topic that the project will be encompassing. This i Some examples 
        the user can narrow down the specifics of what problem they are trying to tackle. Soof topics could be Sports, Law, Education, etc. 
        The second input that you will be provided with is the sort of topic or domain the project will be encompassing. This helps narrow down the problem space the user is interested in exploring. 
        Examples of topics include Sports, Law, Education, Healthcare, Environment, Finance, or Arts.
        Use this topic to guide the idea generation process by focusing on relevant challenges, needs, or innovations within that field. 
        The goal is to create a project idea that feels grounded in the chosen domain, while still being creative and feasible for a student to pursue independently or with a team. 
        If the topic is too broad or unclear, ask a clarifying question to help refine the scope before proposing a solution.
        This is the second input that you will use: {data.project_interest}
        
        The third input that you will be provided with is the types of technical skills the user wants to work with. For example, 
        the user could want to do a projject tthat prioritizes machine learning, or a project that prioritizes full stack development,
        or even a project that prioritizes data visualizations with jupyter noteboook. Take these technical requirements into
        consideration when giving a set of projects for the user, making sure that the outputted projects priortize the technical skills
        that the user wants. Also keep in mind, extremely importantly, that if this input indicates that the user does not want to use
        any technical skills, give the user a set of NON-TECHNICAL projects, that don't invovle coding or technical skills. An example
        of this might be a product startup that doesn't have a technical background. Be clear in understanding the type of technical, or
        non-technical skills that the user might want in the potential project that they are looking for.
        This is the third input that you will use: {data.project_technical}

        The fourth input you will receive reflects the user's current stage of ideation. They may already have a fleshed out idea in mind, a rough idea, or nothing at all:
        If they do have an idea, your job is to refine, validate, or expand on it with clear direction and next steps. 
        If they don’t have any idea, begin by proposing 5-10 creative project ideas based on their inputs to the previous questions.
        In both cases, be proactive in asking clarifying questions if needed, and guide them toward a well-scoped and actionable and practical project.
        The fourth input you will use is: {data.project_potential}
        
        The fifth input that you will be provided with is any additional information that the user sees as important in 
        understanding what project ideas to output. Make sure to take any information given here into consideration when 
        providing the user with project ideas.
        This is the fifth input that you will use: {data.project_additional}

        Remember that you are using these five inputs to give the user 5-10 strong, applicable, creative, and 
        attainable projects for them. Try to provide projects with a variety of difficulty levels, so provide some 
        simple projects and some difficult projects as well. If there isn’t a lot of information in the inputs or 
        information given, then be creative and give a variety of projects that are creative and attainable for the student.

        The output of these ideas should be formatted as a bullet point list with each bullet point being a project idea.
        For each project idea I want The Name of the project idea, labeled 'Project Name:', the concept or the overview of the idea itself,
        labeled 'Project Overview:', the difficulty of the project itself, rating the difficulty as either novice, intermediate, advanced, 
        or somewhere in between, labeling this as 'Project Difficulty:', and lastly how many hours the project should take approximately AND MORE IMPORTANTLY how
        many weeks the project should take approximately, giving a general time range into hours per week and also providing the 
        approximate total number of weeks the project will take. This should be labeled as 'Project Timeline:'.

        One final output request: DO NOT PRINT ANYTHING BEFORE THE IDEAS. For example, I mean don't output or say that you are thinking of ideas, Just
        print the ideas in the format I've asked above. 
        """
    

    # Call Gemini
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    # Clean up Gemini response into a list
    raw_output = response.text.strip()
    ideas = [line.strip("-• ") for line in raw_output.split("\n") if line.strip()]

    return {"ideas": ideas}
