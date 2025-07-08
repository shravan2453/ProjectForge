from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
from pydantic import BaseModel, Field

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
    """Estimates realistic time requirements for college students."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    complexity_level: str = dspy.InputField(desc="Project complexity (simple, medium, complex).")
    technical_skills: List[str] = dspy.InputField(desc="Student's current technical skills.")
    has_team: bool = dspy.InputField(desc="Whether this is a team project.")
    
    estimated_hours: int = dspy.OutputField(desc="Total estimated hours needed for project.")
    weekly_commitment: str = dspy.OutputField(desc="Recommended hours per week (e.g., '8-10 hours').")
    timeline_weeks: int = dspy.OutputField(desc="Suggested project duration in weeks.")

class LearningPathGenerator(dspy.Signature):
    """Creates learning milestones before implementation."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    skill_gaps: str = dspy.InputField(desc="Skills the student needs to develop.")
    recommended_resources: List[str] = dspy.InputField(desc="Available learning resources.")
    
    learning_milestones: List[str] = dspy.OutputField(desc="Ordered list of learning tasks (tutorials, readings, practice exercises).")
    prerequisite_concepts: List[str] = dspy.OutputField(desc="Key concepts to master before starting implementation.")

class MilestoneBreakdown(dspy.Signature):
    """Breaks project into actionable, time-boxed milestones."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    complexity_level: str = dspy.InputField(desc="Project complexity level.")
    estimated_hours: int = dspy.InputField(desc="Total project hours.")
    timeline_weeks: int = dspy.InputField(desc="Project duration in weeks.")
    has_team: bool = dspy.InputField(desc="Whether this is a team project.")
    
    milestone_list: List[Dict[str, Any]] = dspy.OutputField(desc="List of milestones with titles, descriptions, estimated hours, and week assignments.")
    quick_wins: List[str] = dspy.OutputField(desc="Early, achievable tasks to build momentum. If possible, also list tasks that can be completed quickly before tackling each milestone.")

class CheckpointPlanner(dspy.Signature):
    """Creates review points and pivot opportunities."""
    
    milestone_list: List[Dict[str, Any]] = dspy.InputField(desc="Generated project milestones.")
    timeline_weeks: int = dspy.InputField(desc="Project timeline in weeks.")
    has_team: bool = dspy.InputField(desc="Whether this is a team project.")
    
    review_checkpoints: List[Dict[str, Any]] = dspy.OutputField(desc="Scheduled review points with goals and criteria.")
    pivot_opportunities: List[str] = dspy.OutputField(desc="Points where students can change direction if needed.")

class AcademicIntegration(dspy.Signature):
    """Aligns project with academic requirements and deadlines."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    timeline_weeks: int = dspy.InputField(desc="Project duration.")
    has_team: bool = dspy.InputField(desc="Team project flag.")
    
    academic_milestones: List[str] = dspy.OutputField(desc="Academic-specific tasks (documentation, presentations, peer reviews).")
    submission_prep: List[str] = dspy.OutputField(desc="Tasks for final submission preparation.")
    portfolio_items: List[str] = dspy.OutputField(desc="Deliverables suitable for academic portfolios.")

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
            technical_skills=state.technical_skills,
            has_team=state.has_team
        )
        
        # Step 2: Create learning path
        learning_plan = self.learning_path(
            project_type=state.project_type,
            skill_gaps=state.skill_gaps or "",
            recommended_resources=state.recommended_resources
        )
        
        # Step 3: Break down into milestones
        milestones = self.milestone_breakdown(
            project_type=state.project_type,
            complexity_level=state.complexity_level,
            estimated_hours=time_estimate.estimated_hours,
            timeline_weeks=time_estimate.timeline_weeks,
            has_team=state.has_team
        )
        
        # Step 4: Add checkpoints
        checkpoints = self.checkpoint_planner(
            milestone_list=milestones.milestone_list,
            timeline_weeks=time_estimate.timeline_weeks,
            has_team=state.has_team
        )
        
        # Step 5: Academic integration
        academic_items = self.academic_integration(
            project_type=state.project_type,
            timeline_weeks=time_estimate.timeline_weeks,
            has_team=state.has_team
        )
        
        return MilestoneOutput(
            milestones=milestones.milestone_list,
            timeline={
                "estimated_hours": time_estimate.estimated_hours,
                "weekly_commitment": time_estimate.weekly_commitment,
                "timeline_weeks": time_estimate.timeline_weeks
            },
            learning_path=learning_plan.learning_milestones,
            quick_wins=milestones.quick_wins,
            checkpoints=checkpoints.review_checkpoints,
            pivot_opportunities=checkpoints.pivot_opportunities,
            academic_deliverables=academic_items.academic_milestones,
            submission_prep=academic_items.submission_prep,
            portfolio_items=academic_items.portfolio_items
        )