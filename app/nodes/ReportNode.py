from app.state import StateModel
from app.modules.Classifier import Classifier

def report_node(state:StateModel) -> StateModel:
    """Generate project report based on timeline and milestones."""

    report_generator = ReportAssembler()
    updated_state = report_generator.run(state)
    return updated_state
