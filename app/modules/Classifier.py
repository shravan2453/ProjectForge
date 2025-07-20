# TODO: Implement form parsing logic using DSPy to predict project type and complexity (Chain of Thought or Predict)

from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from app.state import StateModel
from pydantic import BaseModel, Field
import logging
class ClassifierOutput(BaseModel):
    """Output data for Classifier."""

    project_type: str = Field(..., description="The classified project type.")
    complexity_level: str = Field(..., description="The AI-generated complexity level based on user's skills and experience.")
    complexity_reasoning: str = Field(..., description="Detailed explanation of why this complexity level was assigned.")
    skill_alignment_score: str = Field(..., description="How well the user's current skills align with project requirements.")
    learning_curve_assessment: str = Field(..., description="Assessment of learning curve steepness for this user.")
    recommended_resources: List[str] = Field(..., description="List of suggested learning resources.")
    skill_gaps: str = Field(..., description="Skills the user should develop for this project.")
    reasoning: str = Field(..., description="The model's reasoning or interpretation of the user's inputs.")

class ProjectTypeClassify(dspy.Signature):
    """Classify the type of Project."""

    project_purpose: str = dspy.InputField(desc="What is the project for?")
    topic_of_interest: str = dspy.InputField(desc="What topic is the user interested in?")
    potential_idea: str = dspy.InputField(desc="Does the user have a specific idea or none at all?")
    time_constraints: str = dspy.InputField(desc="How much time can user dedicate?")
    end_goal: str = dspy.InputField(desc="What is the desired outcome of the project?")

    project_type: str = dspy.OutputField(desc="The classified project type.")
    project_subtype: str = dspy.OutputField(desc="More granular classification")
    suitable_for_portfolio: bool = dspy.OutputField(desc="Is this project suitable for a portfolio and does it support user's goals?")

    

class ComplexityClassify(dspy.Signature):
    """Determines the complexity of a project based on user inputs and experience."""
    project_type: str = dspy.InputField(desc="The determined project type.")
    user_skills: str = dspy.InputField(desc="User's actual technical skills from their profile.")
    user_experience_level: str = dspy.InputField(desc="User's overall experience level (beginner, intermediate, advanced)")
    user_type: str = dspy.InputField(desc="Type of user (e.g., student, professional)")
    technical_skills_wanted: List[str] = dspy.InputField(desc="Technical skills the user wants to apply to this project.")
    past_projects_context: str = dspy.InputField(desc="Information about user's completed projects and experience history.")
    additional_info: str = dspy.InputField(desc="Any additional context the user has provided.")

    project_complexity: str = dspy.OutputField(desc="AI-generated project complexity assessment based on user's skill level and project requirements. Should reflect realistic difficulty for this specific user.")
    complexity_reasoning: str = dspy.OutputField(desc="Detailed explanation of why this complexity level was assigned, considering user's background.")
    skill_alignment_score: str = dspy.OutputField(desc="How well the user's current skills align with project requirements (high/medium/low).")
    learning_curve_assessment: str = dspy.OutputField(desc="Assessment of learning curve steepness for this user.")
    reasoning: str = dspy.OutputField(desc="The model's overall reasoning or interpretation of the user's inputs.")


#TODO:  Later tweak the resources to also include more specific advice based on the user's experience level with the topics they wish to use

class ResourceRecommend(dspy.Signature):
    """Recommends initial resources and learning paths based on project classification."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    project_complexity: str = dspy.InputField(desc="The assessed complexity level.")
    technical_skills: str = dspy.InputField(desc="User's technical background.")
    topic_of_interest: str = dspy.InputField(desc="The subject domain.")
    additional_info: str = dspy.InputField(desc="Any extra context or requirements provided by the user.")

    recommended_resources: str = dspy.OutputField(desc="List of suggested learning resources, tools, or references separated by semicolons like Python tutorial; JavaScript guide; React documentation; etc.")
    skill_gaps: str = dspy.OutputField(desc="Skills the user should develop for this project.")



class Classifier(dspy.Module):
    """
    Classifies the user's project based on their inputs.
    """

    def __init__(self):
        super().__init__()
        self.type_classifier = dspy.Predict(ProjectTypeClassify)
        self.complexity_classifier = dspy.Predict(ComplexityClassify)
        self.resource_recommender = dspy.ChainOfThought(ResourceRecommend)

    def run(self, state: StateModel) -> ClassifierOutput:
        """
        Classify the project based on user inputs (with possible intent refinement hints).
        """ 

        profile_context_dict = state.GetProfileContext()
        
        # Chech if intent refinement is needed
        hints = []
        insufficient_info = False

        if not state.project_goal and not state.interests:
            hints.append("User needs to clarify their project goals and interests.")
            insufficient_info = True
        
        if not state.project_goal:
            hints.append("What specific problem or goal does this project address?")
        
        if not state.interests:
            hints.append("What topics or areas is the user interested in exploring?")
        
        if not state.end_goal:
            hints.append("What outcome do you hope to achieve with this project?")
        
        if not profile_context_dict.get("user_type"):
            hints.append("How much time can you realistically dedicate to this project?")
        
        if insufficient_info:
            state.intent_refinement_needed = True
            state.refinement_hints = hints
            return ClassifierOutput(
                project_type="needs_refinement",
                complexity_level="unknown",
                complexity_reasoning="Need more information",
                skill_alignment_score="Need more information",
                learning_curve_assessment="Need more information",
                recommended_resources=["Intent refinement required"],
                skill_gaps="Insufficient information",
                reasoning="Insufficient information provided, call IntentRefiner"
            )
        
        # Safe time commitment extraction
        time_constraints = "Not specified"

        # get time contstraints from profile context
        hours_per_week = profile_context_dict.get("hours_per_week", None)
        if hours_per_week:
            time_constraints = f"{hours_per_week} hours per week"
        else:
            hints.append("Please clarify your time availability")
        # If any hints were generated, set the intent refinement flag
        if hints:
            state.intent_refinement_needed = True
            state.refinement_hints = hints


        # Classify project type
        type_result = self.type_classifier(
            project_purpose=state.project_goal or "Not specified",
            topic_of_interest=", ".join(state.interests) if state.interests else "Not specified",
            potential_idea=(state.project_data or {}).get("idea", "Not specified"),
            time_constraints=time_constraints,
            end_goal=state.end_goal or "Not specified"
        )
        # TODO: For future implementation when we track completed projects
        # Get past projects context for personalization
        past_projects_context = "No previous projects completed"

       
        completed_count = len(state.completed_tasks) if state.completed_tasks else 0
        if completed_count > 0:
            # Extract project types and 
            # for personalization
            past_project_types = []
            technologies_used = []
            project_outcomes = []

            for task in state.completed_tasks:
                if isinstance(task, dict):
                    past_project_types.append(task.get("project_type", "Unknown"))
                if task.get("technologies"):
                    technologies_used.extend(task.get("technologies", []))
                if task.get("outcome") or task.get("status") == "completed":
                    project_outcomes.append(task.get("outcome", "No outcome specified"))

            past_projects_context = f"User has completed {completed_count} previous projects"
            if past_project_types:
                past_projects_context += f" of types: {', '.join(set(past_project_types))}"
            if technologies_used:
                past_projects_context += f", using technologies: {', '.join(set(technologies_used))}"
            if project_outcomes:
                past_projects_context += f", with: {', '.join(set(project_outcomes))} successful completions"

        # Classify project complexity based on the type, user experience, and skills
        complexity_result = self.complexity_classifier(
            project_type=type_result.project_type,
            user_skills=", ".join(profile_context_dict.get("skill_domains", [])) if profile_context_dict.get("skill_domains") else "No technical skills specified",
            user_experience_level=profile_context_dict.get("experience_level", "beginner"),
            user_type=profile_context_dict.get("user_type", "student"),
            technical_skills_wanted=", ".join(state.technical_skills) if state.technical_skills else "No technical skills specified",
            past_projects_context=past_projects_context,
            additional_info=state.project_data.get("additional_info", "No additional information provided") if state.project_data else "No additional information provided"
        )

        # Recommend resources based on the classification results
        resource_result = self.resource_recommender(
            project_type=type_result.project_type,
            project_complexity=complexity_result.project_complexity,
            technical_skills=", ".join(state.technical_skills) if state.technical_skills else "No technical skills specified",
            topic_of_interest=", ".join(state.interests) if state.interests else "Not specified",
            additional_info=state.project_data.get("additional_info", "No additional information")
        )
        
        # parse the recommended resources output
        resources_list = [r.strip() for r in resource_result.recommended_resources.split(";")] if resource_result.recommended_resources else []

        return ClassifierOutput(
            project_type=type_result.project_type,
            complexity_level=complexity_result.project_complexity,
            complexity_reasoning=complexity_result.complexity_reasoning,
            skill_alignment_score=complexity_result.skill_alignment_score,
            learning_curve_assessment=complexity_result.learning_curve_assessment,
            recommended_resources=resources_list,
            skill_gaps=resource_result.skill_gaps,
            reasoning=complexity_result.reasoning
        )

    