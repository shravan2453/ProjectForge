"""
Test suite for the MilestoneGen DSPy module.

Tests milestone generation, time estimation, and learning path creation
without making actual LLM API calls when possible.
"""

import pytest
from unittest.mock import Mock, patch
from app.modules.MilestoneGen import MilestoneGenerator, MilestoneOutput
from app.state import StateModel
from app.person import PersonProfile


class TestMilestoneGenerator:
    """Test cases for the MilestoneGenerator module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.milestone_gen = MilestoneGenerator()
    
    def test_milestone_generator_initialization(self):
        """Test that MilestoneGenerator initializes correctly."""
        assert self.milestone_gen is not None
        assert hasattr(self.milestone_gen, 'time_estimator')
        assert hasattr(self.milestone_gen, 'learning_path')
        assert hasattr(self.milestone_gen, 'milestone_breakdown')
    
    def test_milestone_generator_output_structure(self, rich_state_model):
        """Test that MilestoneGenerator returns correct MilestoneOutput structure."""
        with patch.object(self.milestone_gen, 'time_estimator') as mock_time, \
             patch.object(self.milestone_gen, 'learning_path') as mock_learning, \
             patch.object(self.milestone_gen, 'milestone_breakdown') as mock_milestones, \
             patch.object(self.milestone_gen, 'checkpoint_planner') as mock_checkpoints, \
             patch.object(self.milestone_gen, 'academic_integration') as mock_academic:
            
            # Mock time estimation
            mock_time.return_value = Mock(
                estimated_hours=120,
                weekly_commitment="10-15 hours",
                timeline_weeks=10
            )
            
            # Mock learning path
            mock_learning.return_value = Mock(
                learning_milestones=["Learn React basics", "Study API fundamentals"]
            )
            
            # Mock milestone breakdown
            mock_milestones.return_value = Mock(
                milestone_list=[
                    {"week": 1, "title": "Setup", "tasks": ["Environment setup"]},
                    {"week": 2, "title": "Backend", "tasks": ["API development"]}
                ],
                quick_wins=["Setup development environment", "Create project structure"]
            )
            
            # Mock checkpoint planner
            mock_checkpoints.return_value = Mock(
                review_checkpoints=[
                    {"week": 2, "type": "milestone review"},
                    {"week": 4, "type": "progress check"}
                ],
                pivot_opportunities=["After backend completion", "Before deployment"]
            )
            
            # Mock academic integration
            mock_academic.return_value = Mock(
                project_deliverables=["Working application", "Documentation"],
                completion_prep=["Final testing", "Code review"],
                portfolio_items=["GitHub repository", "Demo video"]
            )
            
            result = self.milestone_gen.run(rich_state_model)
            
            # Test output type
            assert isinstance(result, MilestoneOutput)
            
            # Test all required fields exist
            assert hasattr(result, 'milestones')
            assert hasattr(result, 'timeline')
            assert hasattr(result, 'learning_path')
            assert hasattr(result, 'quick_wins')
            assert hasattr(result, 'checkpoints')
            assert hasattr(result, 'pivot_opportunities')
            assert hasattr(result, 'project_deliverables')
            assert hasattr(result, 'completion_prep')
            assert hasattr(result, 'portfolio_items')
            
            # Test field types
            assert isinstance(result.milestones, list)
            assert isinstance(result.timeline, dict)
            assert isinstance(result.learning_path, list)
            assert isinstance(result.quick_wins, list)
            assert isinstance(result.checkpoints, list)
            assert isinstance(result.pivot_opportunities, list)
            assert isinstance(result.project_deliverables, list)
            assert isinstance(result.completion_prep, list)
            assert isinstance(result.portfolio_items, list)
            
            # Test field values
            assert len(result.milestones) == 2
            assert result.timeline["estimated_hours"] == 120
            assert result.timeline["timeline_weeks"] == 10
            assert "10-15 hours" in result.timeline["weekly_commitment"]
            assert len(result.learning_path) > 0
            assert len(result.quick_wins) > 0
    
    def test_milestone_generator_technical_skills_conversion(self, rich_state_model):
        """Test that technical_skills list is properly converted to string."""
        # Set technical skills as list
        rich_state_model.technical_skills = ["Python", "React", "PostgreSQL"]
        
        with patch.object(self.milestone_gen, 'time_estimator') as mock_time, \
             patch.object(self.milestone_gen, 'learning_path') as mock_learning, \
             patch.object(self.milestone_gen, 'milestone_breakdown') as mock_milestones, \
             patch.object(self.milestone_gen, 'checkpoint_planner') as mock_checkpoints, \
             patch.object(self.milestone_gen, 'academic_integration') as mock_academic:
            
            mock_time.return_value = Mock(
                estimated_hours=80,
                weekly_commitment="8-12 hours",
                timeline_weeks=8
            )
            
            mock_learning.return_value = Mock(
                learning_milestones=["Learn React basics", "Study API fundamentals"]
            )
            
            mock_milestones.return_value = Mock(
                milestone_list=[{"week": 1, "title": "Start"}],
                quick_wins=["Setup environment"]
            )
            
            mock_checkpoints.return_value = Mock(
                review_checkpoints=[],
                pivot_opportunities=[]
            )
            
            mock_academic.return_value = Mock(
                project_deliverables=["MVP"],
                completion_prep=["Testing"],
                portfolio_items=["GitHub repo"]
            )
            
            result = self.milestone_gen.run(rich_state_model)
            
            # Verify time estimator was called with string
            args, kwargs = mock_time.call_args
            assert 'technical_skills' in kwargs
            technical_skills_arg = kwargs['technical_skills']
            assert isinstance(technical_skills_arg, str)
            assert "Python, React, PostgreSQL" in technical_skills_arg
    
    def test_milestone_generator_empty_skills_handling(self, minimal_state_model):
        """Test MilestoneGenerator with empty technical skills."""
        minimal_state_model.technical_skills = []
        minimal_state_model.project_type = "web-app"
        minimal_state_model.complexity_level = "beginner"
        
        with patch.object(self.milestone_gen, 'time_estimator') as mock_time, \
             patch.object(self.milestone_gen, 'learning_path') as mock_learning, \
             patch.object(self.milestone_gen, 'milestone_breakdown') as mock_milestones, \
             patch.object(self.milestone_gen, 'checkpoint_planner') as mock_checkpoints, \
             patch.object(self.milestone_gen, 'academic_integration') as mock_academic:
            
            mock_time.return_value = Mock(
                estimated_hours=40,
                weekly_commitment="5-8 hours",
                timeline_weeks=6
            )
            
            mock_learning.return_value = Mock(
                learning_milestones=["Learn HTML/CSS basics", "JavaScript fundamentals"],
                prerequisite_concepts=["HTML/CSS basics"]
            )
            
            mock_milestones.return_value = Mock(
                milestone_list=[{"week": 1, "title": "Learn basics"}],
                quick_wins=["Setup basic HTML"]
            )
            
            mock_checkpoints.return_value = Mock(
                review_checkpoints=[],
                pivot_opportunities=[]
            )
            
            mock_academic.return_value = Mock(
                project_deliverables=["Simple website"],
                completion_prep=["Final review"],
                portfolio_items=["Portfolio site"]
            )
            
            result = self.milestone_gen.run(minimal_state_model)
            
            # Verify fallback string was used
            args, kwargs = mock_time.call_args
            assert kwargs['technical_skills'] == "No specific technical skills listed"
            
            assert isinstance(result, MilestoneOutput)
            assert result.timeline["estimated_hours"] == 40


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_milestone_generator_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    milestone_gen = MilestoneGenerator()
    result = milestone_gen.run(rich_state_model)
    
    assert isinstance(result, MilestoneOutput)
    assert result.timeline["estimated_hours"] > 0
    assert result.timeline["timeline_weeks"] > 0
    assert len(result.milestones) > 0