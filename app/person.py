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
    technical_skills: List[str] = Field(default_factory=list, max_items=20, description="Current technical abilities")
    skill_levels: Dict[str, Literal["beginner", "intermediate", "advanced"]] = Field(default_factory=dict, description="Proficiency level for each skill")
    interests: List[str] = Field(default_factory=list, max_items=15, description="Areas of interest and passion")
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
    completed_tasks: List[Dict[str, Any]] = Field(default_factory=list, max_items=1000, description="History of completed work")
    current_milestone: Optional[str] = Field(default=None, description="Currently active milestone")
    progress_notes: List[str] = Field(default_factory=list, max_items=100, description="Personal notes and reflections")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="When person was created")
    last_active: Optional[datetime] = Field(default=None, description="Last activity timestamp")
    project_ids: List[str] = Field(default_factory=list, max_items=50, description="Projects this person is involved in")
    
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
    """Lightweight person profile for AI context."""
    
    # Core info for context
    user_type: Literal["student", "professional", "entrepreneur", "freelancer", "hobbyist"]
    experience_level: Literal["beginner", "intermediate", "advanced"]
    
    # Skills for understanding capability, not direction
    has_technical_background: bool = Field(description="Whether person has any tech experience")
    skill_domains: List[str] = Field(max_items=5, description="General areas like 'programming', 'design', 'business'")
    
    # Constraints for realistic planning
    weekly_hours_available: int = Field(ge=1, le=80)
    work_style: Literal["burst-worker", "steady-progress", "deadline-driven", "flexible"]
    
    # Context for question framing, not project assumptions
    learning_preference: Optional[Literal["hands-on", "theory-first", "example-driven"]] = None
    collaboration_preference: Optional[Literal["solo", "small-team", "large-team", "flexible"]] = None
    
    ai_instruction: str = Field(
        default="Use skill_domains for capability assessment only. Do not assume project direction based on background.",
        description="Instructions for AI on how to use this profile")


class TeamMember(BaseModel):
    """Lightweight reference to a person in a specific project context."""
    person_id: str = Field(..., description="Reference to Person object")
    project_role: str = Field(..., min_length=1, max_length=50, description="Role in this specific project")
    responsibilities: List[str] = Field(default_factory=list, max_items=10, description="Assigned tasks and responsibilities")
    milestones_assigned: List[str] = Field(default_factory=list, max_items=20, description="Milestone IDs assigned to this person")
    contribution_percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Expected workload percentage")
    join_date: datetime = Field(default_factory=datetime.now, description="When they joined this project")
    status: Literal["active", "inactive", "removed"] = Field(default="active", description="Team member status")
    
    @validator("responsibilities")
    def validate_responsibilities(cls, v):
        if v and len(v) != len(set(v)):
            raise ValueError("Duplicate responsibilities not allowed")
        return v