from app.state import StateModel
from app.modules.Classifier import Classifier

def milestone_node(state:StateModel) -> StateModel:
    """Generate project milestones given project details."""

    milestones = MilestoneGenerator()
    updated_state = milestones.run(state)
    return updated_state
