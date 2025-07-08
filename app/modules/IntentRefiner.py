from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from app.state import StateModel
from app.person import PersonProfile

class IntentRefined(BaseModel):
    """Represents a refined user intent after clarification."""

    has_relevant_background: bool = Field(default=False, "Indicates if the user has relevant background knowledge to the project they are currently brainstorming.")
    background_assessment: str = Field(default="", "Provides an assessment of the user's background knowledge related to the project.")
    clarified_intent: str = Field(default="", "Clarified user intent")
    follow_up_questions: List[str] = Field(default_factory=list, "Specific questions to gather missing info")
    suggested_project_types: List[str] = Field(default_factory=list, "Potential project categories this could lead to")
    generated_ideas: List[str] = Field(default_factory=list, "List of generated project ideas with the new clarified intent")
    reasoning: str = Field(default="", "Explanation of the reasoning behind the generated ideas")


class RelevanceAssessment(dspy.Signature):
    """Assesses the relevance of the user's background knowledge to the project."""

    user_input: str = dspy.InputField(desc="User's initial input")
    background_assessment: str = dspy.OutputField(desc="Assessment of the user's background knowledge")
    past_projects: List[str] = dspy.OutputField(desc="List of past projects the user has worked on")
    user_type: str = dspy.OutputField(desc="Type of user (e.g., student, professional)")


    has_relevant_background: bool = dspy.OutputField(desc="Whether user has relevant background for this project")
    background_assessment: str = dspy.OutputField(desc="Detailed assessment of how user's background relates to project")
    advice_level: str = dspy.OutputField(desc="Should be personalized advice, based on their background, needs, and goals, etc.")

    
class IntentClarification(dspy.Signature):
    """Clarifies user intent by asking follow-up questions."""

    user_input: str = dspy.InputField(desc="User's initial input")
    conversation_history: List[str] = dspy.InputField(desc="History of the conversation")
    person_profile: str = dspy.InputField(desc="User's background information as formatted string")
    time_constraints: str = dspy.InputField(desc="User's time constraints as formatted string")

    clarified_intent: str = dspy.OutputField(desc="Clarified user intent")
    follow_up_questions: List[str] = dspy.OutputField(desc="Specific questions to gather missing info")
    suggested_project_types: List[str] = dspy.OutputField(desc="Potential project categories this could lead to")


class IdeaGeneration(dspy.Signature):
    """Generates project ideas based on user input and context."""

    clarified_intent: str = dspy.InputField(desc="Clarified user intent")
    follow_up_questions: str = dspy.InputField(desc="Specific questions to gather missing info")
    suggested_project_types: str = dspy.InputField(desc="Potential project categories this could lead to")

    generated_ideas: List[str] = dspy.OutputField(desc="List of generated project ideas with the new clarified intent")
    reasoning: str = dspy.OutputField(desc="Explanation of the reasoning behind the generated ideas")





class IntentRefiner(dspy.Module):
    """Clarifies and expands vague user inputs before classification."""
    
    def __init__(self):
        super().__init__()
        self.intent_clarifier = dspy.ChainOfThought(IntentClarification)
        self.idea_generator = dspy.ChainOfThought(IdeaGeneration)

        

    def format_person_context(self, profile: PersonProfile) -> str:
        """ Convert Person Profile to string for better DSPy output"""
        context_parts = [
        f"User Type: {profile.user_type}",
        f"Experience Level: {profile.experience_level}",
        f"Technical Background: {'Yes' if profile.has_technical_background else 'No'}",
        f"Skill Domains: {', '.join(profile.skill_domains) if profile.skill_domains else 'Not specified'}",
        f"Weekly Hours Available: {profile.weekly_hours_available}",
        f"Work Style: {profile.work_style}",
    ]
    
    if profile.learning_preference:
        context_parts.append(f"Learning Preference: {profile.learning_preference}")
    if profile.collaboration_preference:
        context_parts.append(f"Collaboration Preference: {profile.collaboration_preference}")

    return "\n".join(context_parts)


        pass

    def run(self, state: StateModel) -> StateModel:
        # Handle vague inputs like "I want to learn programming"
        # Generate specific project suggestions
        # Refine user goals into actionable objectives
        pass