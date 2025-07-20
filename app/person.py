from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
import uuid

class Person(BaseModel):
    """Represents a person involved in projects."""
    
    # Core Identity
    person_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for this person")
    name: str = Field(..., min_length=1, max_length=100, description="Person's full name")
    email: Optional[str] = Field(default=None, description="Contact email")
    user_type: Literal["student", "professional", "entrepreneur", "freelancer", "hobbyist"] = Field(..., description="Person's user type")
    
    # Skills & Experience
    technical_skills: List[str] = Field(default_factory=list, max_length=20, description="Current technical abilities")
    skill_levels: Dict[str, Literal["beginner", "intermediate", "advanced"]] = Field(default_factory=dict, description="Proficiency level for each skill")
    interests: List[str] = Field(default_factory=list, max_length=15, description="Areas of interest and passion")
    experience_level: Literal["beginner", "intermediate", "advanced"] = Field(default="beginner", description="Overall experience level")
    
    # Availability & Constraints
    weekly_hours_available: int = Field(default=10, ge=1, le=168, description="Hours available per week for project work")
    work_style: Literal["burst-worker", "steady-progress", "deadline-driven", "flexible"] = Field(default="steady-progress", description="Preferred working approach")
    preferred_working_hours: List[str] = Field(default_factory=list, description="Preferred work schedule")
    timezone: Optional[str] = Field(default=None, description="Person's timezone")
    
    # Project-Specific Info (should be moved to TeamMember for better separation)
    # TODO: Deprecated - use TeamMember model instead for project-specific data
    role_in_project: Optional[str] = Field(default=None, description="DEPRECATED: Use TeamMember.project_role instead")
    responsibilities: Optional[List[str]] = Field(default=None, description="DEPRECATED: Use TeamMember for project responsibilities")
    milestones_assigned: Optional[List[str]] = Field(default=None, description="DEPRECATED: Use TeamMember for milestone assignments")
    
    # Progress Tracking
    completed_tasks: List[Dict[str, Any]] = Field(default_factory=list, max_length=1000, description="History of completed work")
    current_milestone: Optional[str] = Field(default=None, description="Currently active milestone")
    progress_notes: List[str] = Field(default_factory=list, max_length=100, description="Personal notes and reflections")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="When person was created")
    last_active: Optional[datetime] = Field(default=None, description="Last activity timestamp")
    project_ids: List[str] = Field(default_factory=list, max_length=50, description="Projects this person is involved in")
    
    # Validators
    @validator("email")
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v
    
    @validator("technical_skills")
    def validate_technical_skills(cls, v):
        if v and len(v) != len(set(v)):
            raise ValueError("Duplicate skills not allowed")
        return v
    
    @validator("project_ids")
    def validate_project_ids(cls, v):
        if v and len(v) != len(set(v)):
            raise ValueError("Duplicate project IDs not allowed")
        return v

# Context-specific 
class PersonSummary(BaseModel):
    """Minimal person info for lists and references."""
    person_id: str
    name: str
    user_type: Literal["student", "professional", "entrepreneur", "freelancer", "hobbyist"]
    experience_level: Literal["beginner", "intermediate", "advanced"]

class ProjectMemberProfile(BaseModel):
    """Person info relevant within a project context."""
    person_id: str
    name: str
    technical_skills: List[str]
    experience_level: Literal["beginner", "intermediate", "advanced"]
    weekly_hours_available: int
    work_style: Literal["burst-worker", "steady-progress", "deadline-driven", "flexible"]
    timezone: Optional[str]

class PersonProfile(BaseModel):
    """Lightweight person profile for AI context with time management."""
    
    # Core info for context
    user_type: Literal["student", "professional", "entrepreneur", "freelancer", "hobbyist"]
    experience_level: Literal["beginner", "intermediate", "advanced"]
    timezone: Optional[str] = None

    # Skills for understanding capability, not direction
    has_technical_background: bool = Field(description="Whether person has any experience in the project they are working on")
    skill_domains: List[str] = Field(max_length=50, description="General areas like 'programming', 'design', 'business'")
    
    # Time Management & Availability (merged from TimeCommitment)
    hours_per_week: Optional[int] = Field(default=None, ge=1, le=160, description="Realistic hours per week available for projects")
    preferred_schedule: Optional[str] = Field(default=None, description="Free text: 'evenings after 7pm', 'weekend mornings'")
    work_intensity: Optional[Literal["light", "moderate", "focused", "intensive"]] = Field(default=None, description="Preferred work intensity level")
    consistency_preference: Optional[Literal["daily_small_chunks", "few_long_sessions", "flexible"]] = Field(default=None, description="How they prefer to distribute work time")
    
    # Work Style & Collaboration
    work_style: Literal["burst-worker", "steady-progress", "deadline-driven", "flexible"] = Field(default="steady-progress", description="Overall working approach")
    team_size_preference: Optional[Literal["solo", "small-team", "large-team", "flexible"]] = None
    communication_style: Optional[Literal["real_time", "asynchronous", "hybrid"]] = None
    
    # Learning & Context
    learning_preference: Optional[Literal["hands-on", "theory-first", "example-driven"]] = None
    collaboration_preference: Optional[Literal["solo", "small-team", "large-team", "flexible"]] = None  # Kept for backward compatibility
    
    # Constraints & Limitations
    major_constraints: List[str] = Field(default_factory=list, description="Major time constraints: full_time_job, classes, family, other_projects")
    busy_periods: List[str] = Field(default_factory=list, description="Known busy periods: exam_weeks, work_travel, holidays")

    # Deprecated - keeping for backward compatibility but will be removed
    weekly_hours_available: Optional[int] = Field(default=None, ge=1, le=80, description="DEPRECATED: Use hours_per_week instead")

    ai_instruction: str = Field(
        default="Use skill_domains for capability assessment only. Do not assume project direction based on background.",
        description="Instructions for AI on how to use this profile")

#TODO instead of a TeamMember Model, we can pull the team member's Person Profiles and have the AI acces those instead
class TeamMember(BaseModel):
    """Lightweight reference to a person in a specific project context."""
    person_id: str = Field(..., description="Reference to Person object")
    project_role: str = Field(..., min_length=1, max_length=50, description="Role in this specific project")
    responsibilities: List[str] = Field(default_factory=list, max_length=10, description="Assigned tasks and responsibilities")
    milestones_assigned: List[str] = Field(default_factory=list, max_length=20, description="Milestone IDs assigned to this person")
    contribution_percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Expected workload percentage")
    join_date: datetime = Field(default_factory=datetime.now, description="When they joined this project")
    status: Literal["active", "inactive", "removed"] = Field(default="active", description="Team member status")
    
    @validator("responsibilities")
    def validate_responsibilities(cls, v):
        if v and len(v) != len(set(v)):
            raise ValueError("Duplicate responsibilities not allowed")
        return v