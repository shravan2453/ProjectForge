"""
Test suite for the TimelineScheduler DSPy module.

Tests timeline scheduling, calendar integration, and work block optimization
without making actual LLM API calls when possible.
"""

import pytest
import json
from unittest.mock import Mock, patch
from app.modules.TimelineScheduler import TimelineScheduler, ScheduleOutput
from app.state import StateModel
from app.person import PersonProfile


class TestTimelineScheduler:
    """Test cases for the TimelineScheduler module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.scheduler = TimelineScheduler()
    
    def test_timeline_scheduler_initialization(self):
        """Test that TimelineScheduler initializes correctly."""
        assert self.scheduler is not None
        assert hasattr(self.scheduler, 'scheduler')
        assert hasattr(self.scheduler, 'logger')
    
    def test_timeline_scheduler_output_structure(self, rich_state_model):
        """Test that TimelineScheduler returns correct ScheduleOutput structure.""" 
        with patch.object(self.scheduler, 'scheduler') as mock_scheduler:
            mock_scheduler.return_value = Mock(
                weekly_schedule='{"week1": {"tasks": ["Setup"], "hours": 8}}',
                milestone_timeline="Week 1: Setup",
                scheduling_warnings="No conflicts",
                pacing_recommendations="Maintain pace"
            )
            
            result = self.scheduler.schedule_timeline(rich_state_model)
            
            # Test output type and structure
            assert isinstance(result, ScheduleOutput)
            assert hasattr(result, 'timeline')
            assert hasattr(result, 'milestone_schedule')
            assert hasattr(result, 'deadline_conflicts')
            assert hasattr(result, 'suggested_work_blocks')
            assert hasattr(result, 'timeline_notes')
    
    def test_timeline_scheduler_milestone_index_parameter(self, rich_state_model):
        """Test that current_milestone_index is passed correctly to DSPy."""
        rich_state_model.current_milestone_index = 2
        
        with patch.object(self.scheduler, 'scheduler') as mock_scheduler:
            mock_scheduler.return_value = Mock(
                weekly_schedule='{"week1": {"tasks": ["Current milestone"], "hours": 10}}',
                milestone_timeline="Current: Testing phase",
                scheduling_warnings="",
                pacing_recommendations="Focus on current milestone"
            )
            
            result = self.scheduler.schedule_timeline(rich_state_model)
            
            # Verify current_milestone parameter was passed correctly
            args, kwargs = mock_scheduler.call_args
            assert 'current_milestone' in kwargs
            assert kwargs['current_milestone'] == 2
    
    def test_timeline_scheduler_error_handling(self, rich_state_model):
        """Test error handling when DSPy call fails."""
        with patch.object(self.scheduler, 'scheduler') as mock_scheduler:
            # Simulate DSPy failure
            mock_scheduler.side_effect = Exception("DSPy connection failed")
            
            result = self.scheduler.schedule_timeline(rich_state_model)
            
            # Should return error ScheduleOutput
            assert isinstance(result, ScheduleOutput)
            assert "error" in result.timeline
            assert "DSPy connection failed" in result.timeline["error"]


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_timeline_scheduler_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    scheduler = TimelineScheduler()
    result = scheduler.schedule_timeline(rich_state_model)
    
    assert isinstance(result, ScheduleOutput)
    assert len(result.timeline) > 0