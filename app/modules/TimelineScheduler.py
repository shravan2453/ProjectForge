from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
import json
import logging
from pydantic import BaseModel, Field
from app.state import StateModel 

class ScheduleOutput(BaseModel):
    """Output data from timeline scheduling."""
    timeline: Dict[str, Any] = Field(default_factory=dict, description="Project timeline with milestones and deadlines")
    milestone_schedule: List[str] = Field(default_factory=list, description="Human-readable milestone breakdown")
    deadline_conflicts: List[str] = Field(default_factory=list, description="Scheduling warnings and conflicts")
    suggested_work_blocks: List[Dict[str, Any]] = Field(default_factory=list, description="Recommended work sessions")
    timeline_notes: List[str] = Field(default_factory=list, description="Pacing tips and assumptions")

class TimelineScheduler(dspy.Signature):
    """Creates realistic project timelines considering constraints."""
    milestones: str = dspy.InputField(desc="JSON string of project milestones with durations")
    energy_constraints: str = dspy.InputField(desc="User's availability: low, moderate, or high")
    optimal_work_blocks: str = dspy.InputField(desc="JSON string of available time slots")
    calendar_conflicts: str = dspy.InputField(desc="JSON string of unavailable times")
    team_size: int = dspy.InputField(desc="Number of team members")
    complexity_level: str = dspy.InputField(desc="Project complexity: simple, medium, or complex")
    has_team: bool = dspy.InputField(desc="Whether this is a team project")
    current_milestone: int = dspy.InputField(desc="Index of currently active milestone")
    
    weekly_schedule: str = dspy.OutputField(desc="JSON: {week1: {tasks: [], hours: 8}, week2: {...}}")
    milestone_timeline: str = dspy.OutputField(desc="• Week 1-2: Setup\n• Week 3-4: Development\n...")
    scheduling_warnings: str = dspy.OutputField(desc="Plain text warnings about conflicts or tight deadlines")
    pacing_recommendations: str = dspy.OutputField(desc="Advice on project pacing and time management")
    
class Timeline(dspy.Module):
    """Generates realistic project timelines with calendar integration."""
    
    def __init__(self):
        super().__init__()
        self.scheduler = dspy.ChainOfThought(TimelineScheduler)
        self.logger = logging.getLogger(__name__)
    
    def schedule_timeline(self, state: StateModel) -> ScheduleOutput:
        """Create timeline schedule from state data with error handling."""
        
        try:
            # Get timeline length from existing timeline data or default
            timeline_weeks = state.timeline.get("timeline_weeks", 8) if state.timeline else 8
            
            result = self.scheduler(
                milestones=json.dumps(state.milestones),
                energy_constraints=state.energy_constraints or "moderate",
                optimal_work_blocks=json.dumps(state.optimal_work_blocks),
                calendar_conflicts=json.dumps(state.calendar_conflicts),
                team_size=state.team_size,
                complexity_level=state.complexity_level or "medium",
                has_team=state.has_team
            )
            
            # Safe JSON parsing
            try:
                timeline_data = json.loads(result.project_timeline)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse timeline JSON: {e}")
                timeline_data = {"error": "Invalid timeline format", "raw": result.project_timeline}
            
            return ScheduleOutput(
                timeline=timeline_data,
                milestone_schedule=[result.milestone_schedule],
                deadline_conflicts=[result.deadline_conflicts] if result.deadline_conflicts else [],
                suggested_work_blocks=state.optimal_work_blocks,  # Use existing data
                timeline_notes=[result.timeline_notes] if result.timeline_notes else []
            )
            
        except Exception as e:
            self.logger.error(f"Timeline scheduling failed: {e}")
            return ScheduleOutput(
                timeline={"error": str(e)},
                milestone_schedule=["Timeline generation failed"],
                deadline_conflicts=[f"Error: {str(e)}"],
                suggested_work_blocks=[],
                timeline_notes=["Please try again"]
            )