from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from app.state import StateModel
from app.person import PersonProfile
from pydantic import BaseModel, Field
class IntentRefinedModel(BaseModel):
    """Represents a refined user intent after clarification."""

    has_relevant_background: bool = Field(default=False, description="Indicates if the user has relevant background knowledge to the project they are currently brainstorming.")
    background_assessment: str = Field(default="", description="Provides an assessment of the user's background knowledge related to the project.")
    clarified_intent: str = Field(default="", description="Clarified user intent")
    follow_up_questions: List[str] = Field(default_factory=list, description="Specific questions to gather missing info")
    suggested_project_types: List[str] = Field(default_factory=list, description="Potential project categories this could lead to")
    generated_ideas: List[str] = Field(default_factory=list, description="List of generated project ideas with the new clarified intent")
    reasoning: str = Field(default="", description="Explanation of the reasoning behind the generated ideas")


class IntentClarification(dspy.Signature):
    """Clarifies user intent by asking tailored follow-up questions based on user profile and current context."""

    user_input: str = dspy.InputField(desc="User's initial input")
    conversation_history: List[str] = dspy.InputField(desc="History of the conversation")
    person_profile: str = dspy.InputField(desc="User's background information as formatted string")
    time_constraints: str = dspy.InputField(desc="User's time constraints as formatted string")
    user_type: str = dspy.InputField(desc="Type of user (e.g., student, professional)")
    experience_level: str = dspy.InputField(desc="User's experience level with this specific project/domain and technical background")
    skill_domains: str  = dspy.InputField(desc="User's current skill domains and expertise areas")

    clarified_intent: str = dspy.OutputField(desc="Clarified user intent tailored to user's profile and goals")
    follow_up_questions: List[str] = dspy.OutputField(desc="Specific questions to gather missing info")
    suggested_project_types: List[str] = dspy.OutputField(desc="Project categories appropriate for the user's level and goals")


class IdeaGeneration(dspy.Signature):
    """Generates project ideas based on user input and context."""

    clarified_intent: str = dspy.InputField(desc="Clarified user intent")
    follow_up_questions: str = dspy.InputField(desc="Specific questions to gather missing info")
    suggested_project_types: str = dspy.InputField(desc="Potential project categories this could lead to")

    generated_ideas: Dict[str, List[str]] = dspy.OutputField(desc="Dictionary of generated project ideas with the project with reasoning as to why it would be beneficial to work on this project for the user and how it can benefit them.")


class IntentRefiner(dspy.Module):
    """Clarifies and expands vague user inputs before classification."""
    
    def __init__(self):
        super().__init__()
        
        self.intent_clarifier = dspy.ChainOfThought(IntentClarification)
        self.idea_generator = dspy.ChainOfThought(IdeaGeneration)
        
    

    def run(self, state: StateModel) -> IntentRefinedModel:
        """ Refine user goals into actionable project objectives using PersonProfile strategically"""

        # Use GetProfileContext 
        profile_context_dict = state.GetProfileContext()
        person_context = "\n".join([f"{k}: {v}" for k, v in profile_context_dict.items() if v is not None])

        conversation_history = state.messages if state.messages else []

        user_input_parts = []
        if state.project_goal:
            user_input_parts.append(f"Project goal: {state.project_goal}")
        
        if state.end_goal:
            user_input_parts.append(f"End goal: {state.end_goal}")
        
        if state.interests:
            user_input_parts.append(f"Interests: {', '.join(state.interests)}")
            
        # Use GetProfileContext data instead of manual profile access
        if profile_context_dict:
            context_hints = []
            
            if profile_context_dict.get("user_type"):
                context_hints.append(f"User is a {profile_context_dict['user_type']}")
            if profile_context_dict.get("experience_level"):
                context_hints.append(f"Experience level: {profile_context_dict['experience_level']}")
            if profile_context_dict.get("learning_preference"):
                context_hints.append(f"Prefers {profile_context_dict['learning_preference']} learning")
            if profile_context_dict.get("collaboration_preference"):
                context_hints.append(f"Collaboration style: {profile_context_dict['collaboration_preference']}")
                
            if context_hints:
                user_input_parts.append(f"Context: {'; '.join(context_hints)}")
        
        user_input = "; ".join(user_input_parts) if user_input_parts else "User needs help defining their project"
        


        # Format time constraints from profile context
        time_constraints = "Not specified"
        
        profile_context_dict = state.GetProfileContext()
        hours_per_week = profile_context_dict.get("hours_per_week", None)
        if hours_per_week:
            time_constraints = f"{hours_per_week} hours per week"
        
        # Extract profile data from GetProfileContext for DSPy signature
        user_type = profile_context_dict.get("user_type", "None")
        experience_level = profile_context_dict.get("experience_level", "beginner")
        skill_domains = ", ".join(profile_context_dict.get("skill_domains", [])) if profile_context_dict.get("skill_domains") else "None specified"
        
        # Clarify intent using enhanced signature
        clarification_result = self.intent_clarifier(
            user_input=user_input,
            conversation_history=conversation_history,
            person_profile=person_context,
            time_constraints=time_constraints,
            user_type=user_type,
            experience_level=experience_level,
            skill_domains=skill_domains
        )
        
        # Generate ideas based on clarified intent
        idea_result = self.idea_generator(
            clarified_intent=clarification_result.clarified_intent,
            follow_up_questions=", ".join(clarification_result.follow_up_questions),
            suggested_project_types=", ".join(clarification_result.suggested_project_types)
        )
        
        # Extract generated ideas
        generated_ideas = []
        if isinstance(idea_result.generated_ideas, dict):
            for category, ideas in idea_result.generated_ideas.items():
                if isinstance(ideas, list):
                    generated_ideas.extend(ideas)
                else:
                    generated_ideas.append(str(ideas))
        
        # Assess background relevance using GetProfileContext data
        has_background = bool(profile_context_dict.get("technical_background") and 
                             profile_context_dict.get("skill_domains"))
        
        background_assessment = f"User has {'relevant' if has_background else 'limited'} technical background"
        if profile_context_dict.get("skill_domains"):
            skills = profile_context_dict["skill_domains"]
            if isinstance(skills, list):
                background_assessment += f" in: {', '.join(skills)}"
            else:
                background_assessment += f" in: {skills}"
        
        return IntentRefinedModel(
            has_relevant_background=has_background,
            background_assessment=background_assessment,
            clarified_intent=clarification_result.clarified_intent,
            follow_up_questions=clarification_result.follow_up_questions,
            suggested_project_types=clarification_result.suggested_project_types,
            generated_ideas=generated_ideas,
            reasoning=f"Refined user intent from: '{user_input}' to actionable project objectives"
        )