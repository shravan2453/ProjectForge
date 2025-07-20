from app.state import StateModel
from app.modules.Classifier import Classifier
from app.modules.TimelineScheduler import TimelineScheduler
def timeline_node(state: StateModel) -> StateModel:
    """Generate project timeline based on milestones."""

    timeline_generator = TimelineScheduler()

    schedule_output = timeline_generator.schedule_timeline(state)

    # Convert ScheduleOutput to StateModel
    state.timeline = schedule_output.timeline
    state.optimal_work_blocks = schedule_output.suggested_work_blocks
    state.calendar_conflicts = schedule_output.deadline_conflicts
    state.project_data.get("milestone_schedule", []).append(schedule_output.milestone_schedule)
    state.project_data.get("timeline_notes", []).append(schedule_output.timeline_notes)

    return state
