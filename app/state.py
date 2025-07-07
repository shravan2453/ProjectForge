from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime

# Update in state.py
class TimeCommitment(BaseModel):
    """Comprehensive time availability and work preferences."""
    
    # Basic availability
    hours_per_week: Optional[int] = Field(None, ge=1, le=160, description="Realistic hours per week")
    preferred_schedule: Optional[str] = Field(None, description="Free text: 'evenings after 7pm', 'weekend mornings'")
    
    # Work style
    work_intensity: Optional[Literal["light", "moderate", "focused", "intensive"]] = None
    consistency_preference: Optional[Literal["daily_small_chunks", "few_long_sessions", "flexible"]] = None
    
    # Coordination
    timezone: Optional[str] = None
    collaboration_style: Optional[Literal["real_time", "asynchronous", "hybrid"]] = None
    
    # Constraints
    major_constraints: List[str] = Field(default_factory=list)
    # ["full_time_job", "classes", "family", "other_projects"]
    
    busy_periods: List[str] = Field(default_factory=list)
    # ["exam_weeks", "work_travel", "holidays"]





class StateModel(BaseModel):


    # Conversation Tracking
    user_id: str
    session_id: str
    messages: List[str] = Field(default_factory=list)
    current_topic: Optional[str] = None
    conversation_context: Dict[str, Any] = Field(default_factory=dict)
    session_start_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None


    # Project Management
    user_type: Optional[Literal["student", "professional", "entrepreneur", "freelancer", "hobbyist"]] = None  # Type of user for tailored experience
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
    time_commitment: Optional[TimeCommitment] = None  # User's available time commitment level
    end_goal: Optional[str] = None  # User's desired outcome for the project

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
    checkpoints: List[str] = Field(default_factory=list)  # Saved workflow checkpoints for review
    preferred_tone: Optional[Literal["peer", "coach", "pm", "founder", "cheerleader"]] = None  # AI assistant communication style
    current_milestone_index: Optional[int] = None  # Index of the currently active milestone
    status: Optional[Literal["idle", "awaiting_input", "executing_milestone", "needs_review", "done"]] = "idle"  # Current execution status
    execution_history: Optional[List[Dict[str, Any]]] = Field(default_factory=list)  # History of completed actions and results

    # Classification Results
    project_completeness: float = Field(default=0.0, ge=0.0, le=1.0)  # How complete the project definition is (0-1)
    complexity_level: Optional[Literal["simple", "medium", "complex"]] = None  # AI-assessed project difficulty level
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
