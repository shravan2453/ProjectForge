from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy
import json
import logging
from pydantic import BaseModel, Field
from app.state import StateModel

class ReportOutput(BaseModel):
    """Comprehensive project report output."""
    executive_summary: str = Field(..., description="High-level project overview for quick reading")
    project_overview: Dict[str, Any] = Field(default_factory=dict, description="Structured project details")
    timeline_summary: List[str] = Field(default_factory=list, description="Week-by-week project breakdown")
    team_responsibilities: List[str] = Field(default_factory=list, description="Who does what in the project")
    learning_roadmap: List[str] = Field(default_factory=list, description="Skills development path (depends on individual/team experience with topic)")
    resource_prioritization: Dict[str, str] = Field(default_factory=dict, description="Which resources to use when (resource_name: timing/phase)")
    resource_compilation: List[str] = Field(default_factory=list, description="All recommended resources and tools")
    success_metrics: List[str] = Field(default_factory=list, description="How to measure project completion")
    risk_assessment: List[str] = Field(default_factory=list, description="Potential challenges and solutions")
    project_alignment: List[str] = Field(default_factory=list, description="How project meets user's goals and requirements")

class ProjectSummaryGenerator(dspy.Signature):
    """Creates executive summary of the entire project plan."""
    
    project_type: str = dspy.InputField(desc="Classified project category")
    project_goal: str = dspy.InputField(desc="User's specific project objective")
    complexity_level: str = dspy.InputField(desc="AI-assessed difficulty level")
    timeline_weeks: int = dspy.InputField(desc="Total project duration")
    team_size: int = dspy.InputField(desc="Number of team members")
    key_milestones: str = dspy.InputField(desc="JSON of major project milestones")
    
    executive_summary: str = dspy.OutputField(desc="Concise 2-3 paragraph project overview")
    project_scope: str = dspy.OutputField(desc="What the project includes and excludes")

class TeamRoleAnalyzer(dspy.Signature):
    """Analyzes team structure and defines responsibilities."""

    has_team: bool = dspy.InputField(desc="Whether this is a team project")
    team_size: int = dspy.InputField(desc="Number of team members")
    team_members: str = dspy.InputField(desc="JSON of team member details")
    milestones: str = dspy.InputField(desc="JSON of project milestones")
    complexity_level: str = dspy.InputField(desc="Project difficulty level")
    
    role_assignments: str = dspy.OutputField(desc="Detailed breakdown of who does what")
    collaboration_plan: str = dspy.OutputField(desc="How team members will work together")

class LearningPathSynthesizer(dspy.Signature):
    """Combines all learning elements into cohesive roadmap."""
    
    skill_gaps: str = dspy.InputField(desc="Skills user needs to develop")
    learning_path: str = dspy.InputField(desc="JSON of ordered learning tasks")
    recommended_resources: str = dspy.InputField(desc="JSON of suggested resources")
    project_deliverables: str = dspy.InputField(desc="JSON of project requirements and deliverables")
    
    integrated_roadmap: str = dspy.OutputField(desc="Complete learning journey from start to finish")
    resource_prioritization: str = dspy.OutputField(desc="JSON dictionary mapping resource names to when they should be used")

class RiskAndSuccessAnalyzer(dspy.Signature):
    """Identifies potential challenges and defines success criteria."""
    
    complexity_level: str = dspy.InputField(desc="Project difficulty assessment")
    timeline_weeks: int = dspy.InputField(desc="Project duration")
    time_constraints: str = dspy.InputField(desc="User's time/availability constraints")
    calendar_conflicts: str = dspy.InputField(desc="JSON of scheduling conflicts")
    has_team: bool = dspy.InputField(desc="Whether team coordination is needed")
    
    risk_factors: str = dspy.OutputField(desc="Potential challenges and mitigation strategies")
    success_criteria: str = dspy.OutputField(desc="Clear metrics for project completion")
    contingency_plans: str = dspy.OutputField(desc="What to do if things go wrong")

class GoalAlignmentAnalyzer(dspy.Signature):
    """Ensures project meets user's goals and requirements."""
    
    learning_goal: str = dspy.InputField(desc="User's learning or professional objectives")
    project_type: str = dspy.InputField(desc="Classified project category")
    project_deliverables: str = dspy.InputField(desc="JSON of project requirements and deliverables")
    completion_prep: str = dspy.InputField(desc="JSON of completion preparation tasks")
    portfolio_items: str = dspy.InputField(desc="JSON of portfolio-worthy deliverables")
    
    goal_value: str = dspy.OutputField(desc="How project advances user's goals")
    success_alignment: str = dspy.OutputField(desc="How project meets user's success criteria")

class ReportAssembler(dspy.Module):
    """Generates comprehensive project reports from all collected data."""
    
    def __init__(self):
        super().__init__()
        self.summary_generator = dspy.ChainOfThought(ProjectSummaryGenerator)
        self.team_analyzer = dspy.ChainOfThought(TeamRoleAnalyzer)
        self.learning_synthesizer = dspy.ChainOfThought(LearningPathSynthesizer)
        self.risk_analyzer = dspy.ChainOfThought(RiskAndSuccessAnalyzer)
        self.goal_analyzer = dspy.ChainOfThought(GoalAlignmentAnalyzer)
        self.logger = logging.getLogger(__name__)
    
    def generate_report(self, state: StateModel) -> ReportOutput:
        """Generate comprehensive project report from complete state."""
        
        try:
            # Validate we have enough data
            if not state.project_type or not state.milestones:
                raise ValueError("Insufficient project data for report generation")
            
            # Extract timeline weeks safely
            timeline_weeks = state.timeline.get("timeline_weeks", 0) if state.timeline else 0
            
            # Step 1: Generate executive summary
            summary_result = self.summary_generator(
                project_type=state.project_type,
                project_goal=state.project_goal or "Complete project successfully",
                complexity_level=state.complexity_level or "medium",
                timeline_weeks=timeline_weeks,
                team_size=state.team_size,
                key_milestones=json.dumps(state.milestones[:3])  # Top 3 milestones
            )
            
            # Step 2: Analyze team structure
            team_result = self.team_analyzer(
                has_team=state.has_team,
                team_size=state.team_size,
                team_members=json.dumps(state.team_members),
                milestones=json.dumps(state.milestones),
                complexity_level=state.complexity_level or "medium"
            )
            
            # Step 3: Synthesize learning path
            learning_result = self.learning_synthesizer(
                skill_gaps=state.skill_gaps or "No specific gaps identified",
                learning_path=json.dumps(state.learning_path),
                recommended_resources=json.dumps(state.recommended_resources),
                project_deliverables=json.dumps(state.project_deliverables)
            )
            
            # Step 4: Analyze risks and success criteria
            risk_result = self.risk_analyzer(
                complexity_level=state.complexity_level or "medium",
                timeline_weeks=timeline_weeks,
                time_constraints=state.time_constraints or "moderate",
                calendar_conflicts=json.dumps(state.calendar_conflicts),
                has_team=state.has_team
            )
            
            # Step 5: Analyze goal alignment
            goal_result = self.goal_analyzer(
                learning_goal=state.learning_goal or "Complete project successfully",
                project_type=state.project_type,
                project_deliverables=json.dumps(state.project_deliverables),
                completion_prep=json.dumps(state.completion_prep),
                portfolio_items=json.dumps(state.portfolio_items)
            )
            
            # Parse resource prioritization safely
            try:
                resource_priority_dict = json.loads(learning_result.resource_prioritization)
                if not isinstance(resource_priority_dict, dict):
                    resource_priority_dict = {}
            except (json.JSONDecodeError, AttributeError):
                resource_priority_dict = {}
            
            return ReportOutput(
                executive_summary=summary_result.executive_summary,
                project_overview={
                    "type": state.project_type,
                    "complexity": state.complexity_level,
                    "duration": f"{timeline_weeks} weeks",
                    "team_size": state.team_size,
                    "scope": summary_result.project_scope
                },
                timeline_summary=self._format_timeline_summary(state),
                team_responsibilities=[team_result.role_assignments, team_result.collaboration_plan],
                learning_roadmap=[learning_result.integrated_roadmap],
                resource_prioritization=resource_priority_dict,
                resource_compilation=state.recommended_resources,
                success_metrics=[risk_result.success_criteria],
                risk_assessment=[risk_result.risk_factors, risk_result.contingency_plans],
                project_alignment=[goal_result.goal_value, goal_result.success_alignment]
            )
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return ReportOutput(
                executive_summary=f"Report generation encountered an error: {str(e)}",
                project_overview={"error": str(e)},
                timeline_summary=["Report generation failed"],
                team_responsibilities=["Unable to analyze team structure"],
                learning_roadmap=["Learning path unavailable"],
                resource_prioritization={},
                resource_compilation=[],
                success_metrics=["Success criteria unavailable"],
                risk_assessment=["Risk analysis unavailable"],
                project_alignment=["Goal alignment unavailable"]
            )
    
    def _format_timeline_summary(self, state: StateModel) -> List[str]:
        """Format timeline into readable summary."""
        try:
            summary = []
            for i, milestone in enumerate(state.milestones[:5], 1):  # Top 5 milestones
                title = milestone.get("title", f"Milestone {i}")
                week = milestone.get("week", i)
                summary.append(f"Week {week}: {title}")
            return summary
        except:
            return ["Timeline summary unavailable"]