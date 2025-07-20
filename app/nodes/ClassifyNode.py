from app.state import StateModel
from app.modules.Classifier import Classifier

def classify_node(state: StateModel) -> StateModel:
    """Classify project type and complexity."""

    classifier = Classifier()
    classifier_output = classifier.run(state)
    
    # Convert ClassifierOutput to StateModel
    state.project_type = classifier_output.project_type
    state.complexity_level = classifier_output.complexity_level
    state.recommended_resources = classifier_output.recommended_resources
    state.skill_gaps = classifier_output.skill_gaps
    state.reasoning = classifier_output.reasoning

    # Store additional complexity assesment data in conversation_context
    state.conversation_context.update({
        "complexity_reasoning": classifier_output.complexity_reasoning,
        "skill_alignment_score": classifier_output.skill_alignment_score,
        "learning_curve_assessment": classifier_output.learning_curve_assessment
    })

    
    return state
