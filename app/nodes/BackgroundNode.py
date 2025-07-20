from app.state import StateModel
from app.modules.BackgroundAssesor import BackgroundAssessor

def background_assesor_node(state: StateModel) -> StateModel:
    """Assess background knowledge and resources for the project."""

      # No assessment needed


    # 
    assessor = BackgroundAssessor()
    assessment_output = assessor.assess_background(state)

    state.has_relevant_background = assessment_output.has_relevant_background
    state.background_assessment = assessment_output.background_assessment

    if not state.conversation_context:
        state.conversation_context = {}
    
    state.conversation_context.update({
        "advice_level": assessment_output.advice_level,
        "background_reasoning": assessment_output.reasoning
    })
    
        

    return state