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
    deadline_conflicts: List[Dict[str, Any]] = Field(default_factory=list, description="Scheduling warnings and conflicts")
    suggested_work_blocks: List[Dict[str, Any]] = Field(default_factory=list, description="Recommended work sessions")
    timeline_notes: List[str] = Field(default_factory=list, description="Pacing tips and assumptions")

class TimelineCreator(dspy.Signature):
    """Creates realistic project timelines considering constraints."""
    milestones: str = dspy.InputField(desc="JSON string of project milestones with durations")
    optimal_work_blocks: str = dspy.InputField(desc="JSON string of available time slots")
    calendar_conflicts: str = dspy.InputField(desc="JSON string of unavailable times")
    team_size: str = dspy.InputField(desc="Number of team members")
    complexity_level: str = dspy.InputField(desc="Project complexity: simple, medium, or complex")
    has_team: str = dspy.InputField(desc="Whether this is a team project (True/False) (no other text)")
    current_milestone: str = dspy.InputField(desc="Index of currently active milestone")
    
    weekly_schedule: str = dspy.OutputField(desc="Valid JSON only. Format: {\"week1\": {\"tasks\": [\"task1\"], \"hours\": 8}, \"week2\": {\"tasks\": [\"task2\"], \"hours\": 10}}. Must end with closing brace.")
    milestone_timeline: str = dspy.OutputField(desc="• Week 1-2: Setup\n• Week 3-4: Development\n...")
    scheduling_warnings: str = dspy.OutputField(desc="Plain text warnings about conflicts or tight deadlines")
    pacing_recommendations: str = dspy.OutputField(desc="Advice on project pacing and time management")
    
class TimelineScheduler(dspy.Module):
    """Generates realistic project timelines with calendar integration."""
    
    def __init__(self):
        super().__init__()
        self.scheduler = dspy.ChainOfThought(TimelineCreator)
        self.logger = logging.getLogger(__name__)
    
    def schedule_timeline(self, state: StateModel) -> ScheduleOutput:
        """Create timeline schedule from state data with error handling."""
        
        try:
            # Get timeline length from existing timeline data or default
            timeline_weeks = state.timeline.get("timeline_weeks", 8) if state.timeline else 8
            
            result = self.scheduler(
                milestones=json.dumps(state.milestones),
                optimal_work_blocks=json.dumps(state.optimal_work_blocks),
                calendar_conflicts=json.dumps(state.calendar_conflicts),
                team_size=str(state.team_size),
                complexity_level=state.complexity_level or "medium",
                has_team=str(state.has_team),
                current_milestone=str(state.current_milestone_index or 0)
            )
            
            # Safe JSON parsing with fallback
            def parse_timeline_json(json_string):
                try:
                    # First try direct parsing
                    return json.loads(json_string)
                except json.JSONDecodeError:
                    # Try to fix truncated JSON
                    try:
                        # Add missing closing braces if needed
                        fixed_json = json_string.rstrip()
                        if not fixed_json.endswith('}'):
                            # Count open braces vs close braces
                            open_count = fixed_json.count('{')
                            close_count = fixed_json.count('}')
                            missing_braces = open_count - close_count
                            fixed_json += '}' * missing_braces
                        return json.loads(fixed_json)
                    except:
                        # Create fallback timeline from milestones
                        timeline = {}
                        for i, milestone in enumerate(state.milestones[:8], 1):
                            week_key = f"week{i}"
                            timeline[week_key] = {
                                "tasks": [milestone.get("title", f"Milestone {i}")],
                                "hours": milestone.get("estimated_hours", 8)
                            }
                        return timeline if timeline else {"week1": {"tasks": ["Project work"], "hours": 8}}
            
            timeline_data = parse_timeline_json(result.weekly_schedule)
            
            # Parse deadline conflicts into structured format
            deadline_conflicts_list = []
            if result.scheduling_warnings:
                deadline_conflicts_list.append({
                    "type": "scheduling_warning",
                    "description": result.scheduling_warnings,
                    "severity": "medium",
                    "suggested_resolution": result.pacing_recommendations
                })
            
            return ScheduleOutput(
                timeline=timeline_data,
                milestone_schedule=[result.milestone_timeline],
                deadline_conflicts=deadline_conflicts_list,
                suggested_work_blocks=state.optimal_work_blocks,  # Use existing data
                timeline_notes=[result.pacing_recommendations] if result.pacing_recommendations else []
            )
            
        except Exception as e:
            self.logger.error(f"Timeline scheduling failed: {e}")
            return ScheduleOutput(
                timeline={"error": str(e)},
                milestone_schedule=["Timeline generation failed"],
                deadline_conflicts=[{"type": "error", "description": f"Error: {str(e)}", "severity": "high"}],
                suggested_work_blocks=[],
                timeline_notes=["Please try again"]
            )