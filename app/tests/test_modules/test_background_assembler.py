"""
Test suite for the BackgroundAssessor DSPy module.

Tests background assessment, relevance analysis, and personalized advice
without making actual LLM API calls when possible.
"""

import pytest
from unittest.mock import Mock, patch
from app.modules.BackgroundAssesor import BackgroundAssessor, BackgroundAssessmentOutput
from app.state import StateModel
from app.person import PersonProfile


class TestBackgroundAssessor:
    """Test cases for the BackgroundAssessor module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.assessor = BackgroundAssessor()
    
    def test_background_assessor_initialization(self):
        """Test that BackgroundAssessor initializes correctly."""
        assert self.assessor is not None
        assert hasattr(self.assessor, 'assessor')
    
    def test_background_assessor_output_structure(self, rich_state_model):
        """Test that BackgroundAssessor returns correct BackgroundAssessmentOutput structure."""
        with patch.object(self.assessor, 'assessor') as mock_assessor:
            mock_assessor.return_value = Mock(
                has_relevant_background=True,
                background_assessment="User has strong programming foundation",
                advice_level="Focus on advanced patterns and system design"
            )
            
            result = self.assessor.assess_background(rich_state_model)
            
            # Test output type and required fields
            assert isinstance(result, BackgroundAssessmentOutput)
            assert hasattr(result, 'has_relevant_background')
            assert hasattr(result, 'background_assessment')
            assert hasattr(result, 'advice_level')
            assert hasattr(result, 'reasoning')
            
            # Test field types and values
            assert isinstance(result.has_relevant_background, bool)
            assert isinstance(result.background_assessment, str)
            assert result.has_relevant_background == True
    
    def test_background_assessor_completed_tasks_integration(self, rich_state_model):
        """Test that completed tasks are properly converted and passed."""
        rich_state_model.completed_tasks = [
            {
                "project_type": "web-app",
                "status": "completed",
                "technologies": ["React", "Node.js"]
            },
            {
                "project_type": "data-analysis", 
                "status": "completed",
                "technologies": ["Python", "Pandas"]
            }
        ]
        
        with patch.object(self.assessor, 'assessor') as mock_assessor:
            mock_assessor.return_value = Mock(
                has_relevant_background=True,
                background_assessment="Proven track record with completed projects",
                advice_level="Ready for more complex challenges"
            )
            
            result = self.assessor.assess_background(rich_state_model)
            
            # Verify past projects were converted to string description
            args, kwargs = mock_assessor.call_args
            past_projects_arg = kwargs['past_projects']
            
            assert isinstance(past_projects_arg, str)
            assert "completed 2 projects" in past_projects_arg.lower()
            assert "web-app (completed)" in past_projects_arg
    
    def test_background_assessor_no_completed_tasks(self, rich_state_model):
        """Test assessment with no completed tasks."""
        rich_state_model.completed_tasks = []
        
        with patch.object(self.assessor, 'assessor') as mock_assessor:
            mock_assessor.return_value = Mock(
                has_relevant_background=True,
                background_assessment="Strong skills but no completed projects yet",
                advice_level="Time to apply skills to a real project"
            )
            
            result = self.assessor.assess_background(rich_state_model)
            
            # Verify past projects shows no previous work
            args, kwargs = mock_assessor.call_args
            assert kwargs['past_projects'] == "No previous projects completed"


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_background_assessor_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    assessor = BackgroundAssessor()
    result = assessor.assess_background(rich_state_model)
    
    assert isinstance(result, BackgroundAssessmentOutput)
    assert isinstance(result.has_relevant_background, bool)