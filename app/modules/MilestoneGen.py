from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from pydantic import BaseModel, Field
from app.state import StateModel
# TODO be able to regenerate the milestones with user input


class MilestoneOutput(BaseModel):
    """Output data from milestone generation."""
    milestones: List[Dict[str, Any]] = Field(..., description="Project milestones with titles, descriptions, estimated hours, and week assignments")
    timeline: Dict[str, Any] = Field(..., description="Project timeline containing estimated hours, weekly commitment, and total duration in weeks")
    learning_path: List[str] = Field(..., description="Ordered list of learning tasks, tutorials, and prerequisite concepts to master before implementation")
    quick_wins: List[str] = Field(default_factory=list, description="Early achievable tasks to build momentum and confidence at project start")
    checkpoints: List[Dict[str, Any]] = Field(default_factory=list, description="Scheduled review points with goals and criteria for assessing progress")
    pivot_opportunities: List[str] = Field(default_factory=list, description="Strategic points where students can change project direction if needed")
    project_deliverables: List[str] = Field(..., description="Key outputs and deliverables for project completion")
    completion_prep: List[str] = Field(..., description="Final steps to wrap up and deliver the project")
    portfolio_items: List[str] = Field(default_factory=list, description="Deliverables suitable for academic portfolios and career showcasing")

class TimeEstimator(dspy.Signature):
    # TODO: Possibly add more context for more accurate Time Estimations
    """Estimates realistic time requirements for the user."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    complexity_level: str = dspy.InputField(desc="Project complexity (simple, medium, complex).")
    technical_skills: str = dspy.InputField(desc="Student's current technical skills as comma-separated string.")
    has_team: str = dspy.InputField(desc="Whether this is a team project. (True/False) (no other text)")
    
    estimated_hours: int = dspy.OutputField(desc="Total estimated hours needed for project.")
    weekly_commitment: str = dspy.OutputField(desc="Recommended hours per week (e.g., '8-10 hours').")
    timeline_weeks: int = dspy.OutputField(desc="Suggested project duration in weeks.")

class LearningPathGenerator(dspy.Signature):
    """Creates learning milestones before implementation."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    skill_gaps: str = dspy.InputField(desc="Skills the student needs to develop.")
    recommended_resources: str = dspy.InputField(desc="Available learning resources separated by semicolons like: Python tutorial; JavaScript guide; React documentation; etc.")
    
    learning_milestones: List[str] = dspy.OutputField(desc="Ordered list of learning tasks (tutorials, readings, practice exercises).")
    prerequisite_concepts: List[str] = dspy.OutputField(desc="Key concepts to master before starting implementation.")

class MilestoneBreakdown(dspy.Signature):
    """Breaks project into actionable, time-boxed milestones."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    complexity_level: str = dspy.InputField(desc="Project complexity level.")
    estimated_hours: int = dspy.InputField(desc="Total project hours.")
    timeline_weeks: int = dspy.InputField(desc="Project duration in weeks.")
    has_team: str = dspy.InputField(desc="Whether this is a team project. (True/False) (no other text)")
    
    milestone_list: List[Dict[str, Any]] = dspy.OutputField(desc="List of milestones with titles, descriptions, estimated hours, and week assignments.")
    quick_wins: List[str] = dspy.OutputField(desc="Early, achievable tasks to build momentum. If possible, also list tasks that can be completed quickly before tackling each milestone.")

class CheckpointPlanner(dspy.Signature):
    """Creates review points and pivot opportunities."""
    
    milestone_list: List[Dict[str, Any]] = dspy.InputField(desc="Generated project milestones.")
    timeline_weeks: int = dspy.InputField(desc="Project timeline in weeks.")
    has_team: str = dspy.InputField(desc="Whether this is a team project. (True/False) (no other text)")
    
    review_checkpoints: List[Dict[str, Any]] = dspy.OutputField(desc="Scheduled review points with goals and criteria.")
    pivot_opportunities: List[str] = dspy.OutputField(desc="Points where students can change direction if needed.")

class AcademicIntegration(dspy.Signature):
    """Aligns project with academic requirements and deadlines."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    timeline_weeks: int = dspy.InputField(desc="Project duration.")
    has_team: str = dspy.InputField(desc="Whether this is a team project. (True/False) (no other text)")
    
    academic_milestones: List[str] = dspy.OutputField(desc="Academic-specific tasks (documentation, presentations, peer reviews).")
    submission_prep: List[str] = dspy.OutputField(desc="Tasks for final submission preparation.")
    portfolio_items: List[str] = dspy.OutputField(desc="Deliverables suitable for academic portfolios.")
    project_deliverables: List[str] = dspy.OutputField(desc= "Key outputs and deliverables for project completion.")
    completion_prep: List[str] = dspy.OutputField(desc="Final steps to wrap up and deliver the project.")

class MilestoneGenerator(dspy.Module):
    """Complete milestone generation system for college students."""
    
    def __init__(self):
        super().__init__()
        # Initialize components
        self.time_estimator = dspy.ChainOfThought(TimeEstimator)
        self.learning_path = dspy.ChainOfThought(LearningPathGenerator)
        self.milestone_breakdown = dspy.ChainOfThought(MilestoneBreakdown)
        self.checkpoint_planner = dspy.ChainOfThought(CheckpointPlanner)
        self.academic_integration = dspy.ChainOfThought(AcademicIntegration)


    def run(self, state:StateModel) -> MilestoneOutput:
        """Generate comprehensive milestone plan for students."""
        
        # Step 1: Estimate time requirements
        time_estimate = self.time_estimator(
            project_type=state.project_type,
            complexity_level=state.complexity_level,
            technical_skills=", ".join(state.technical_skills) if state.technical_skills else "No technical skills specified",
            has_team=str(state.has_team)
        )
        
        # Step 2: Create learning path
        learning_plan = self.learning_path(
            project_type=state.project_type,
            skill_gaps=state.skill_gaps or "",
            recommended_resources=", ".join(state.recommended_resources) if state.recommended_resources else "No resources available"
        )
        
        # Step 3: Break down into milestones
        milestones = self.milestone_breakdown(
            project_type=state.project_type,
            complexity_level=state.complexity_level,
            estimated_hours=str(time_estimate.estimated_hours),
            timeline_weeks=str(time_estimate.timeline_weeks),
            has_team=str(state.has_team)
        )
        
        # Step 4: Add checkpoints
        checkpoints = self.checkpoint_planner(
            milestone_list=str(milestones.milestone_list),
            timeline_weeks=str(time_estimate.timeline_weeks),
            has_team=str(state.has_team)
        )
        
        # Step 5: Academic integration
        academic_items = self.academic_integration(
            project_type=state.project_type,
            timeline_weeks=str(time_estimate.timeline_weeks),
            has_team=str(state.has_team)
        )
        
        # Parse DSPy string outputs back to Python lists
        def parse_milestone_list(milestone_string):
            """Parse milestone string into list of dictionaries."""
            if not milestone_string or milestone_string == "[]":
                return []
            try:
                # Try to parse as JSON first
                import json
                return json.loads(milestone_string)
            except:
                # If JSON parsing fails, create basic milestone structure
                lines = [line.strip() for line in milestone_string.split('\n') if line.strip()]
                milestones = []
                for i, line in enumerate(lines[:10], 1):  # Limit to 10 milestones
                    if line.startswith(str(i)) or '-' in line:
                        title = line.split('-', 1)[-1].strip() if '-' in line else line
                        milestones.append({
                            "title": title,
                            "description": title,
                            "estimated_hours": 8,
                            "week": i
                        })
                return milestones

        def parse_string_list(list_string):
            """Parse string list into Python list."""
            if not list_string or list_string == "[]":
                return []
            # Split by newlines and clean up
            items = [item.strip('- ').strip() for item in list_string.split('\n') if item.strip()]
            return [item for item in items if item and not item.isdigit()]

        def parse_checkpoint_list(checkpoint_string):
            """Parse checkpoint string into list of dictionaries."""
            if not checkpoint_string or checkpoint_string == "[]":
                return []
            try:
                import json
                return json.loads(checkpoint_string)
            except:
                # Create basic checkpoint structure
                items = parse_string_list(checkpoint_string)
                checkpoints = []
                for i, item in enumerate(items[:5], 1):  # Limit to 5 checkpoints
                    checkpoints.append({
                        "week": i * 2,
                        "goal": item,
                        "criteria": f"Complete {item}"
                    })
                return checkpoints

        return MilestoneOutput(
            milestones=parse_milestone_list(str(milestones.milestone_list)),
            timeline={
                "estimated_hours": time_estimate.estimated_hours,
                "weekly_commitment": time_estimate.weekly_commitment,
                "timeline_weeks": time_estimate.timeline_weeks
            },
            learning_path=parse_string_list(str(learning_plan.learning_milestones)),
            quick_wins=parse_string_list(str(milestones.quick_wins)),
            checkpoints=parse_checkpoint_list(str(checkpoints.review_checkpoints)),
            pivot_opportunities=parse_string_list(str(checkpoints.pivot_opportunities)),
            project_deliverables=parse_string_list(str(academic_items.project_deliverables)),
            completion_prep=parse_string_list(str(academic_items.completion_prep)),
            portfolio_items=parse_string_list(str(academic_items.portfolio_items))
        )
