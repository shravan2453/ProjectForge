from app.state import StateModel
from app.modules.Classifier import Classifier
from app.modules.ReportAssembler import ReportAssembler
def report_node(state:StateModel) -> StateModel:
    """Generate project report based on timeline and milestones."""

    report_generator = ReportAssembler()
    report = report_generator.generate_report(state)
    
    # Convert ReportOutput to StateModel
    state.executive_summary = report.executive_summary
    state.project_overview = report.project_overview
    state.timeline_summary = report.timeline_summary
    state.team_responsibilities = report.team_responsibilities
    state.learning_roadmap = report.learning_roadmap
    state.resource_prioritization = report.resource_prioritization
    state.resource_compilation = report.resource_compilation
    state.success_metrics = report.success_metrics
    state.risk_assessment = report.risk_assessment
    state.project_alignment = report.project_alignment
    
    return state