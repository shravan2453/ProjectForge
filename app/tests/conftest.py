"""
Shared pytest fixtures and configuration for ProjectForge tests.

This file is automatically loaded by pytest and provides common test utilities
that can be used across all test modules.
"""

import pytest
from typing import Dict, Any, List
from app.state import StateModel
from app.person import PersonProfile


@pytest.fixture
def sample_person_profile():
    """Create a sample PersonProfile for testing."""
    return PersonProfile(
        user_type="student",
        experience_level="intermediate",
        has_technical_background=True,
        skill_domains=["programming", "web-development", "python"],
        timezone="UTC",
        hours_per_week=15,
        work_style="steady-progress",
        learning_preference="hands-on",
        major_constraints=["classes", "part-time-job"],
        busy_periods=["exam-weeks"]
    )


@pytest.fixture
def minimal_state_model(sample_person_profile):
    """Create a minimal StateModel for basic testing."""
    return StateModel(
        user_id="test_user_123",
        session_id="test_session_456",
        person_profile=sample_person_profile,
        project_goal="Build a web application",
        interests=["web development", "python"],
        technical_skills=["Python", "HTML", "CSS"],
        end_goal="Learn full-stack development"
    )


@pytest.fixture
def rich_state_model(sample_person_profile):
    """Create a fully populated StateModel for comprehensive testing."""
    return StateModel(
        user_id="test_user_123",
        session_id="test_session_456",
        person_profile=sample_person_profile,
        project_goal="Build a full-stack e-commerce platform",
        project_type="web-app",
        complexity_level="intermediate",
        interests=["web development", "e-commerce", "databases"],
        technical_skills=["Python", "React", "PostgreSQL", "Docker"],
        end_goal="Create a production-ready application for portfolio",
        milestones=[
            {"id": 1, "title": "Setup development environment", "duration_weeks": 1},
            {"id": 2, "title": "Build user authentication", "duration_weeks": 2},
            {"id": 3, "title": "Implement product catalog", "duration_weeks": 3}
        ],
        completed_tasks=[
            {
                "project_type": "web-app",
                "status": "completed",
                "technologies": ["Flask", "SQLite"],
                "outcome": "Successfully deployed blog application"
            },
            {
                "project_type": "data-analysis", 
                "status": "completed",
                "technologies": ["Pandas", "Matplotlib"],
                "outcome": "Created data visualization dashboard"
            }
        ],
        recommended_resources=["MDN Web Docs", "React Documentation", "PostgreSQL Tutorial"],
        skill_gaps="Need to learn React hooks and state management",
        reasoning="User has solid foundation but needs frontend framework experience"
    )


@pytest.fixture
def mock_dspy_responses():
    """Mock DSPy module responses for testing without actual LLM calls."""
    return {
        "classifier": {
            "project_type": "web-app",
            "complexity_level": "intermediate", 
            "complexity_reasoning": "Good match for user's current skill level",
            "skill_alignment_score": "high",
            "learning_curve_assessment": "moderate - some new concepts to learn",
            "recommended_resources": ["React docs", "Node.js tutorial"],
            "skill_gaps": "Frontend state management",
            "reasoning": "Well-suited project for skill development"
        },
        "intent_refiner": {
            "clarified_intent": "Build an e-commerce platform to learn full-stack development",
            "follow_up_questions": ["What type of products will you sell?", "Do you need payment integration?"],
            "suggested_project_types": ["web-app", "full-stack-project"],
            "generated_ideas": ["Online bookstore", "Digital marketplace", "Subscription service"],
            "has_relevant_background": True,
            "background_assessment": "Strong programming foundation with web development experience",
            "reasoning": "Clear project vision with good technical foundation"
        },
        "milestone_gen": {
            "estimated_hours": 120,
            "weekly_commitment": "10-15 hours",
            "timeline_weeks": 10,
            "milestones": ["Planning & Setup", "Backend Development", "Frontend Development", "Testing & Deployment"],
            "learning_path": ["React fundamentals", "API design", "Database modeling", "Deployment strategies"],
            "reasoning": "Realistic timeline based on user's availability and experience"
        }
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing various scenarios."""
    return {
        "simple_project": {
            "idea": "Personal blog website",
            "complexity": "beginner",
            "technologies": ["HTML", "CSS", "JavaScript"]
        },
        "complex_project": {
            "idea": "Multi-tenant SaaS platform",
            "complexity": "advanced", 
            "technologies": ["React", "Node.js", "PostgreSQL", "Docker", "AWS"]
        },
        "team_project": {
            "idea": "Mobile app for local businesses",
            "complexity": "intermediate",
            "technologies": ["React Native", "Firebase"],
            "team_size": 3
        }
    }


# Test utilities
def assert_state_model_valid(state: StateModel):
    """Helper function to validate StateModel instances in tests."""
    assert state.user_id is not None
    assert state.session_id is not None
    assert isinstance(state.messages, list)
    assert isinstance(state.conversation_context, dict)
    assert isinstance(state.milestones, list)
    assert isinstance(state.technical_skills, list)


def create_mock_state(**overrides) -> StateModel:
    """Create a StateModel with custom overrides for specific test scenarios."""
    defaults = {
        "user_id": "test_user",
        "session_id": "test_session",
        "project_goal": "Test project",
        "interests": ["testing"],
        "technical_skills": ["Python"]
    }
    defaults.update(overrides)
    return StateModel(**defaults)