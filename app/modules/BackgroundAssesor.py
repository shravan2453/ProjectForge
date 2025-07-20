from typing import Dict, Any, List, Literal
import dspy
from pydantic import BaseModel, Field
from app.state import StateModel
from app.person import PersonProfile

class RelevanceAssessment(dspy.Signature):
    """Assesses the relevance of the user's background knowledge to the project."""

    user_input: str = dspy.InputField(desc="User's initial input")
    user_skills: str = dspy.InputField(desc="List of user's skills")
    past_projects: str = dspy.InputField(desc="Description of past projects the user has worked on")
    user_type: str = dspy.InputField(desc="Type of user (e.g., student, professional)")


    has_relevant_background: Literal["True", "False"] = dspy.OutputField(desc="Whether user has relevant background for this project. Answer with exactly 'True' or 'False' (no other text)")
    background_assessment: str = dspy.OutputField(desc="Detailed assessment of how user's background relates to project")
    advice_level: str = dspy.OutputField(desc="Should be personalized advice, based on their background, needs, and goals, etc.")


class BackgroundAssessmentOutput(BaseModel):
    """Output data from background assessment."""
    has_relevant_background: bool = Field(..., description="Whether user has relevant background for this project")
    background_assessment: str = Field(..., description="Detailed assessment of how user's background relates to project")
    advice_level: str = Field(..., description="Personalized advice based on background and goals")
    reasoning: str = Field(..., description="Explanation of the assessment")


class BackgroundAssessor(dspy.Module):
    """Assesses user background relevance to project."""
    
    def __init__(self):
        super().__init__()
        self.assessor = dspy.ChainOfThought(RelevanceAssessment)
    
    def assess_background(self, state: StateModel) -> BackgroundAssessmentOutput:
        """Assess user's background relevance using GetProfileContext."""
        
        # Use GetProfileContext method for consistent data access
        profile_context_dict = state.GetProfileContext()
        
        # Safely extract profile data
        user_skills = ", ".join(profile_context_dict.get("skill_domains", [])) if profile_context_dict.get("skill_domains") else "No technical skills specified"
        user_type = profile_context_dict.get("user_type", "student")
        
        # Convert completed tasks to string for DSPy input
        past_projects_str = "No previous projects completed"

        if state.completed_tasks:
            project_descriptions = []
            for task in state.completed_tasks:
                if isinstance(task, dict):
                    project_type = task.get("project_type", "Unknown project")
                    status = task.get("status", "Unknown status")
                    project_descriptions.append(f"{project_type} ({status})")

            if project_descriptions:
                past_projects_str = f"Completed {len(project_descriptions)} projects: " + ", ".join(project_descriptions)
                
        # Build user input context
        user_input = f"Project goal: {state.project_goal or 'Not specified'}"
        if state.interests:
            user_input += f"; Interests: {', '.join(state.interests)}"
        
        result = self.assessor(
            user_input=user_input,
            user_skills=user_skills,
            past_projects=past_projects_str,
            user_type=user_type
        )

        # Parse boolean response from LLM (may return string)
        has_background = result.has_relevant_background == 'True'
        
        
        return BackgroundAssessmentOutput(
            has_relevant_background=has_background,
            background_assessment=result.background_assessment,
            advice_level=result.advice_level,
            reasoning=f"Background assessment based on: {user_type} with skills in {user_skills}"
        )