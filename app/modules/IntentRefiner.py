from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from app.state import StateModel

class IntentClarification(dspy.Signature):
    """Clarifies user intent by asking follow-up questions."""

    user_input: str = dspy.InputField(desc="User's initial input")
    conversation_history: List[str] = dspy.InputField(desc="History of the conversation")
    person_profile: PersonProfile = dspy.InputField(desc="User's background information")
    time_constraints: List[str]= dspy.InputField(desc="User's time constraints")




    clarified_intent: str = dspy.OutputField(desc="Clarified user intent")
    follow_up_questions: str = dspy.OutputField(desc="Specific questions to gather missing info")
    suggested_project_types: str = dspy.OutputField(desc="Potential project categories this could lead to")






class IntentRefiner(dspy.Module):
    """Clarifies and expands vague user inputs before classification."""
    
    def __init__(self):
        super().__init__()
        self.intent_clarifier = dspy.ChainOfThought(IntentClarification)
        self.idea_generator = dspy.ChainOfThought(IdeaGeneration)
    
    def run(self, state: StateModel) -> StateModel:
        # Handle vague inputs like "I want to learn programming"
        # Generate specific project suggestions
        # Refine user goals into actionable objectives