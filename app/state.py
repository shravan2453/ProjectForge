from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
from app.person import PersonProfile


class StateModel(BaseModel):
    """The State that gets passed around the LangGraph workflow."""

    # Person Profile
    person_profile: Optional[PersonProfile] = Field(default=None, description="User's background information and skills")

    # Conversation Tracking
    user_id: str
    session_id: str
    messages: List[str] = Field(default_factory=list)
    current_topic: Optional[str] = None
    conversation_context: Dict[str, Any] = Field(default_factory=dict)
    session_start_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None


    # Intent Refinement Tracking
    intent_refinement_needed: bool = Field(default=False, description="Whether the IntentRefiner node should be called")
    refinement_hints: List[str] = Field(default_factory=list, description="Hints for IntentRefiner about what needs clarification")

    # Project Management
    # user_type: Removed - use person_profile.user_type
    learning_goal: Optional[str] = None  # What the user wants to achieve through this project
    project_goal: Optional[str] = None  # Specific project objective or outcome
    project_type: Optional[str] = None  # Classified project category (web-app, data-analysis, etc.)
    project_context: Optional[Literal["academic", "professional", "personal", "startup", "client-work"]] = None  # Context for project execution
    idea_origin: Optional[Literal["user-input", "generated", "team-brainstorm", "inspired-by-interest"]] = None  # How the project idea was conceived
    project_data: Dict[str, Any] = Field(default_factory=dict)  # Raw project information and metadata
    extracted_project: Dict[str, Any] = Field(default_factory=dict)  # Processed project details from form/input
    interests: List[str] = Field(default_factory=list)  # User's areas of interest and topics
    technical_skills: List[str] = Field(default_factory=list)  # User's current technical abilities
    milestones: List[Dict[str, Any]] = Field(default_factory=list)  # Project milestones with details and deadlines
    timeline: Dict[str, Any] = Field(default_factory=dict)  # Project schedule and time estimates
    learning_path: List[str] = Field(default_factory=list)  # Ordered learning tasks before implementation
    quick_wins: List[str] = Field(default_factory=list)  # Early achievable tasks to build momentum
    pivot_opportunities: List[str] = Field(default_factory=list)  # Points where project direction can change
    project_deliverables: List[str] = Field(default_factory=list)  # Key outputs and deliverables for project completion
    completion_prep: List[str] = Field(default_factory=list)  # Final steps to wrap up and deliver the project
    portfolio_items: List[str] = Field(default_factory=list)  # Deliverables suitable for portfolios and career showcasing
    potential_ideas: List[str] = Field(default_factory=list)  # Generated or suggested project ideas
    info_gaps: List[str] = Field(default_factory=list)  # Missing information needed for project planning
    reflections: List[str] = Field(default_factory=list)  # User reflections and learning insights
    confidence_level: Optional[float] = Field(default=None, ge=0.0, le=1.0)  # User's confidence in project success (0-1)
    # time_commitment merged into PersonProfile for simplicity
    end_goal: Optional[str] = None  # User's desired outcome for the project
    
    # Intent Refinement Results
    generated_ideas: List[str] = Field(default_factory=list)  # AI-generated project ideas
    suggested_project_types: List[str] = Field(default_factory=list)  # Suggested project categories
    follow_up_questions: List[str] = Field(default_factory=list)  # Questions for user clarification
    has_relevant_background: bool = False  # Whether user has relevant background
    background_assessment: Optional[str] = None  # Assessment of user's background
    
    # Past Projects & Experience (for AI personalization)
    completed_tasks: List[Dict[str, Any]] = Field(default_factory=list, description="History of completed projects and tasks for AI personalization")
    
    # Report Generation Results
    executive_summary: Optional[str] = None  # Project executive summary
    project_overview: Dict[str, Any] = Field(default_factory=dict)  # Detailed project overview
    timeline_summary: List[str] = Field(default_factory=list)  # Summary of project timeline
    team_responsibilities: List[str] = Field(default_factory=list)  # Team member responsibilities
    learning_roadmap: List[str] = Field(default_factory=list)  # Learning path and resources
    resource_prioritization: Dict[str, str] = Field(default_factory=dict)  # Prioritized resources
    resource_compilation: List[str] = Field(default_factory=list)  # Compiled resource list
    success_metrics: List[str] = Field(default_factory=list)  # Project success indicators
    risk_assessment: List[str] = Field(default_factory=list)  # Identified risks and mitigation
    project_alignment: List[str] = Field(default_factory=list)  # Project alignment analysis

    # Team Information
    has_team: bool = False  # Whether this is a team project
    team_members: List[Dict[str, Any]] = Field(default_factory=list)  # Team member details and roles
    team_size: int = 1  # Number of people working on the project

    # Calendar Integration
    calendar_data: Dict[str, Any] = Field(default_factory=dict)  # User's calendar information and events
    team_availability: Dict[str, Any] = Field(default_factory=dict)  # When team members are available
    optimal_work_blocks: List[Dict[str, Any]] = Field(default_factory=list)  # Best times for focused work
    calendar_conflicts: List[Dict[str, Any]] = Field(default_factory=list)  # Scheduling conflicts to avoid

    # Workflow State
    current_node: str = "start"  # Current position in the LangGraph workflow
    workflow_phase: Literal[
        "collecting", "classifying", "generating", "scheduling",
        "reviewing", "executing", "reflecting", "publishing", "completed"
    ] = "collecting"  # Current phase of the project development process
    retry_count: int = 0  # Number of times current operation has been retried
    checkpoints: List[Dict[str, Any]] = Field(default_factory=list)  # Saved workflow checkpoints for review
    preferred_tone: Optional[Literal["peer", "coach", "pm", "founder", "cheerleader"]] = None  # AI assistant communication style
    current_milestone_index: Optional[int] = None  # Index of the currently active milestone
    status: Optional[Literal["idle", "awaiting_input", "executing_milestone", "needs_review", "done"]] = "idle"  # Current execution status
    execution_history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)  # History of completed actions and results

    # Classification Results
    project_completeness: float = Field(default=0.0, ge=0.0, le=1.0)  # How complete the project definition is (0-1)
    complexity_level: str = Field(default = "beginner", description="Project complexity level")
    needs_more_info: bool = False  # Whether additional information is needed to proceed
    recommended_resources: List[str] = Field(default_factory=list)  # AI-suggested learning resources and tools
    skill_gaps: Optional[str] = None  # Skills the user should develop for this project
    reasoning: Optional[str] = None  # AI's reasoning for complexity and resource recommendations

    # Error Handling
    errors: List[str] = Field(default_factory=list)  # Critical errors that need attention
    warnings: List[str] = Field(default_factory=list)  # Non-critical issues and warnings
    log: Optional[Dict[str, List[str]]] = Field(default_factory=dict)  # Detailed operation logs for debugging

    # Publishing Layer
    ready_for_publish: Optional[bool] = False  # Whether project is ready to be shared publicly
    publish_slug: Optional[str] = None  # URL-friendly identifier for published project
    is_public: Optional[bool] = False  # Whether project is publicly visible



    # 🧪 Custom Validators
    @validator("team_size")
    def validate_team_size(cls, v):
        if v < 1:
            raise ValueError("You must have at least one team member.")
        return v

    @validator("project_completeness")
    def validate_project_completeness(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("project_completeness must be between 0.0 and 1.0")
        return v
    

    # Profile Context Methods

    def GetProfileContext(self) -> Dict[str, Any]:
        """Return all of the profile data - let AI ignore irrelevant information."""
        if not self.person_profile:
            return {}
        
        profile = self.person_profile
        
        return {
            "user_type": profile.user_type,
            "experience_level": profile.experience_level,
            "technical_background": profile.has_technical_background,
            "skill_domains": profile.skill_domains,
            "timezone": profile.timezone,
            # Time management (merged from TimeCommitment)
            "hours_per_week": profile.hours_per_week,
            "preferred_schedule": profile.preferred_schedule,
            "work_intensity": profile.work_intensity,
            "consistency_preference": profile.consistency_preference,
            # Work style & collaboration
            "work_style": profile.work_style,
            "team_size_preference": profile.team_size_preference,
            "communication_style": profile.communication_style,
            # Learning preferences
            "learning_preference": profile.learning_preference,
            "collaboration_preference": profile.collaboration_preference,
            # Constraints
            "major_constraints": profile.major_constraints,
            "busy_periods": profile.busy_periods,
            # Backward compatibility
            "weekly_hours_available": profile.weekly_hours_available or profile.hours_per_week
        }