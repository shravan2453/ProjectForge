from app.state import StateModel
from app.modules.MilestoneGen import MilestoneGenerator
def milestone_node(state:StateModel) -> StateModel:
    """Generate project milestones given project details."""


    milestone_generator = MilestoneGenerator()
    milestone_output = milestone_generator.run(state)

    # Convert MilestoneOutput to StateModel
    state.milestones = milestone_output.milestones
    state.timeline = milestone_output.timeline
    state.learning_path = milestone_output.learning_path
    state.quick_wins = milestone_output.quick_wins
    state.checkpoints = milestone_output.checkpoints
    state.pivot_opportunities = milestone_output.pivot_opportunities
    state.project_deliverables = milestone_output.project_deliverables
    state.completion_prep = milestone_output.completion_prep
    state.portfolio_items = milestone_output.portfolio_items

    return state
