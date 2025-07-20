"""
Mock StateModel instances for different testing scenarios.

This file provides pre-configured StateModel instances that represent
common user scenarios and edge cases for comprehensive testing.
"""

from app.state import StateModel
from app.person import PersonProfile
from .mock_data import create_mock_completed_tasks


def create_beginner_student_state() -> StateModel:
    """StateModel for a beginner student with minimal experience."""
    profile = PersonProfile(
        user_type="student",
        experience_level="beginner", 
        has_technical_background=False,
        skill_domains=["basic-programming"],
        hours_per_week=8,
        work_style="steady-progress",
        major_constraints=["classes", "part-time-job"],
        busy_periods=["exam-weeks", "finals"]
    )
    
    return StateModel(
        user_id="student_001",
        session_id="session_beginner_001",
        person_profile=profile,
        project_goal="Learn web development by building my first website",
        interests=["web development", "design"],
        technical_skills=["HTML basics"],
        end_goal="Get an internship in web development",
        completed_tasks=[],  # No previous projects
        complexity_level="beginner"
    )


def create_intermediate_professional_state() -> StateModel:
    """StateModel for an intermediate professional with some experience.""" 
    profile = PersonProfile(
        user_type="professional",
        experience_level="intermediate",
        has_technical_background=True,
        skill_domains=["programming", "web-development", "databases"],
        hours_per_week=15,
        work_style="deadline-driven", 
        major_constraints=["full-time-job"],
        busy_periods=["work-travel", "project-deadlines"]
    )
    
    return StateModel(
        user_id="prof_002", 
        session_id="session_prof_002",
        person_profile=profile,
        project_goal="Build a full-stack application to advance my career",
        project_type="web-app",
        interests=["full-stack development", "career advancement", "modern frameworks"],
        technical_skills=["Python", "JavaScript", "SQL", "React basics"],
        end_goal="Transition to senior developer role",
        completed_tasks=create_mock_completed_tasks(2),
        complexity_level="intermediate",
        milestones=[
            {"id": 1, "title": "Backend API development", "duration_weeks": 3},
            {"id": 2, "title": "Frontend React app", "duration_weeks": 4},
            {"id": 3, "title": "Integration and deployment", "duration_weeks": 2}
        ],
        recommended_resources=["React documentation", "Node.js tutorials", "System design guides"],
        skill_gaps="Advanced React patterns, system design, deployment automation"
    )


def create_experienced_entrepreneur_state() -> StateModel:
    """StateModel for an experienced entrepreneur building a business."""
    profile = PersonProfile(
        user_type="entrepreneur", 
        experience_level="advanced",
        has_technical_background=True,
        skill_domains=["programming", "business", "product-management", "system-design"],
        hours_per_week=25,
        work_style="burst-worker",
        team_size_preference="small-team",
        major_constraints=["investor-meetings", "team-management"]
    )
    
    return StateModel(
        user_id="entrepreneur_003",
        session_id="session_ent_003", 
        person_profile=profile,
        project_goal="Build MVP for SaaS platform to validate business idea",
        project_type="saas-platform",
        project_context="startup",
        interests=["entrepreneurship", "scalable systems", "user experience"],
        technical_skills=["Python", "React", "PostgreSQL", "AWS", "Docker"],
        end_goal="Launch profitable SaaS business",
        has_team=True,
        team_size=3,
        completed_tasks=create_mock_completed_tasks(5),
        complexity_level="advanced",
        milestones=[
            {"id": 1, "title": "Market research and user interviews", "duration_weeks": 2},
            {"id": 2, "title": "MVP backend development", "duration_weeks": 4}, 
            {"id": 3, "title": "Frontend and user onboarding", "duration_weeks": 3},
            {"id": 4, "title": "Beta testing and iteration", "duration_weeks": 3},
            {"id": 5, "title": "Launch preparation", "duration_weeks": 2}
        ],
        timeline={"timeline_weeks": 14, "launch_date": "Q2 2024"},
        recommended_resources=[
            "Lean Startup methodology",
            "SaaS metrics and KPIs", 
            "Scalable system architecture",
            "Customer development guides"
        ]
    )


def create_minimal_state() -> StateModel:
    """Minimal StateModel with only required fields for edge case testing."""
    return StateModel(
        user_id="minimal_user",
        session_id="minimal_session"
        # All other fields will use their defaults
    )


def create_intent_refinement_needed_state() -> StateModel:
    """StateModel that should trigger intent refinement due to insufficient info."""
    profile = PersonProfile(
        user_type="student",
        experience_level="beginner",
        has_technical_background=False,
        skill_domains=[]  # Empty skills
    )
    
    return StateModel(
        user_id="vague_user",
        session_id="vague_session", 
        person_profile=profile,
        project_goal="",  # Empty goal
        interests=[],  # No interests
        technical_skills=[],  # No skills
        end_goal="",  # No end goal
        intent_refinement_needed=True,
        refinement_hints=[
            "What specific problem do you want to solve?",
            "What topics interest you most?", 
            "What outcome do you hope to achieve?"
        ]
    )


def create_team_project_state() -> StateModel:
    """StateModel for a team-based project scenario."""
    profile = PersonProfile(
        user_type="student",
        experience_level="intermediate",
        has_technical_background=True,
        skill_domains=["programming", "web-development"],
        team_size_preference="small-team",
        communication_style="hybrid"
    )
    
    return StateModel(
        user_id="team_lead_001",
        session_id="team_session_001",
        person_profile=profile,
        project_goal="Build a collaborative project management tool for student teams",
        project_type="web-app",
        has_team=True,
        team_size=4,
        team_members=[
            {"name": "Alice", "role": "Frontend Developer", "skills": ["React", "CSS"]},
            {"name": "Bob", "role": "Backend Developer", "skills": ["Node.js", "MongoDB"]}, 
            {"name": "Charlie", "role": "UI/UX Designer", "skills": ["Figma", "User Research"]},
            {"name": "David", "role": "DevOps", "skills": ["Docker", "AWS"]}
        ],
        interests=["team collaboration", "productivity tools", "user experience"],
        technical_skills=["JavaScript", "React", "Node.js", "Git"],
        complexity_level="intermediate"
    )


def create_state_with_errors() -> StateModel:
    """StateModel that might trigger various error conditions for error handling tests.""" 
    return StateModel(
        user_id="error_test_user",
        session_id="error_test_session",
        project_goal="Build something impossible",
        complexity_level="expert-impossible",  # Unrealistic complexity
        technical_skills=["Beginner HTML"],  # Skills don't match complexity
        end_goal="Become senior developer in 1 week",  # Unrealistic timeline
        errors=["Complexity mismatch detected"],
        warnings=["Timeline may be too ambitious"]
    )


# Utility function to get state by scenario name
def get_mock_state(scenario: str) -> StateModel:
    """Get a pre-configured StateModel for a specific test scenario."""
    state_map = {
        "beginner_student": create_beginner_student_state,
        "intermediate_professional": create_intermediate_professional_state,
        "experienced_entrepreneur": create_experienced_entrepreneur_state,
        "minimal": create_minimal_state,
        "intent_refinement": create_intent_refinement_needed_state,
        "team_project": create_team_project_state,
        "error_conditions": create_state_with_errors
    }
    
    creator_func = state_map.get(scenario)
    if creator_func:
        return creator_func()
    else:
        raise ValueError(f"Unknown state scenario: {scenario}")


# List of all available scenarios for test parametrization
AVAILABLE_SCENARIOS = [
    "beginner_student",
    "intermediate_professional", 
    "experienced_entrepreneur",
    "minimal",
    "intent_refinement",
    "team_project",
    "error_conditions"
]