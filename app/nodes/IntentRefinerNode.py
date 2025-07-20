from app.state import StateModel
from app.modules.IntentRefiner import IntentRefiner

def intent_refiner_node(state: StateModel) -> StateModel:
    """Refine user intent when called by LangGraph workflow."""

    if not state.intent_refinement_needed:
        return state  # No refinement needed

    refiner = IntentRefiner()
    refinement_output = refiner.run(state)


    if refinement_output:
        state.project_goal = refinement_output.clarified_intent
        state.generated_ideas = refinement_output.generated_ideas
        state.suggested_project_types = refinement_output.suggested_project_types
        state.follow_up_questions = refinement_output.follow_up_questions
        state.reasoning = refinement_output.reasoning
        
        # Update background assessment
        state.has_relevant_background = refinement_output.has_relevant_background
        state.background_assessment = refinement_output.background_assessment
        
        # Safely update project_data
        if not state.project_data:
            state.project_data = {}
        state.project_data["refined_intent"] = refinement_output.clarified_intent

        # Clear refinement hints after processing
        if state.refinement_hints:
            state.refinement_hints.clear()
        state.intent_refinement_needed = False

    return state