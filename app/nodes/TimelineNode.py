from app.state import StateModel
from app.modules.Classifier import Classifier

def timeline_node(state:StateModel) -> StateModel:
    """Generate project timeline based on milestones."""

    timeline_generator = TimelineScheduler()
    updated_state = timeline_generator.run(state)
    return updated_state
