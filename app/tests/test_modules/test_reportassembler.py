"""
Test suite for the ReportAssembler DSPy module.

Tests comprehensive report generation including executive summary,
resource compilation, and risk assessment without making actual LLM API calls.
"""

import pytest
import json
from unittest.mock import Mock, patch
from app.modules.ReportAssembler import ReportAssembler, ReportOutput
from app.state import StateModel
from app.person import PersonProfile


class TestReportAssembler:
    """Test cases for the ReportAssembler module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.report_assembler = ReportAssembler()
    
    def test_report_assembler_initialization(self):
        """Test that ReportAssembler initializes correctly."""
        assert self.report_assembler is not None
        assert hasattr(self.report_assembler, 'summary_generator')
        assert hasattr(self.report_assembler, 'team_analyzer')
        assert hasattr(self.report_assembler, 'learning_synthesizer')
        assert hasattr(self.report_assembler, 'risk_analyzer')
        assert hasattr(self.report_assembler, 'goal_analyzer')
    
    def test_report_assembler_output_structure(self, rich_state_model):
        """Test that ReportAssembler returns correct ReportOutput structure."""
        with patch.object(self.report_assembler, 'summary_generator') as mock_exec, \
             patch.object(self.report_assembler, 'team_analyzer') as mock_team, \
             patch.object(self.report_assembler, 'learning_synthesizer') as mock_learning, \
             patch.object(self.report_assembler, 'risk_analyzer') as mock_risk, \
             patch.object(self.report_assembler, 'goal_analyzer') as mock_goal:
            
            # Mock all DSPy responses
            mock_exec.return_value = Mock(
                executive_summary="8-week full-stack development project",
                project_scope="E-commerce platform for local artisans"
            )
            
            mock_team.return_value = Mock(
                role_assignments="Solo project - developer handles all aspects",
                collaboration_plan="Individual work with periodic reviews"
            )
            
            mock_learning.return_value = Mock(
                integrated_roadmap="Comprehensive learning path from basics to advanced",
                resource_prioritization='{"React docs": "critical", "Node.js guides": "important"}'
            )
            
            mock_risk.return_value = Mock(
                risk_factors="Timeline risk: Complex features may take longer",
                success_criteria="Functional app, responsive design",
                contingency_plans="Weekly reviews, scope management"
            )
            
            mock_goal.return_value = Mock(
                project_alignment="Aligns with full-stack career goals"
            )
            
            result = self.report_assembler.generate_report(rich_state_model)
            
            # Test output type and required fields
            assert isinstance(result, ReportOutput)
            assert hasattr(result, 'executive_summary')
            assert hasattr(result, 'project_overview')
            assert hasattr(result, 'timeline_summary')
            assert hasattr(result, 'team_responsibilities')
            assert hasattr(result, 'learning_roadmap')
            assert hasattr(result, 'resource_prioritization')
            assert hasattr(result, 'resource_compilation')
            assert hasattr(result, 'success_metrics')
            assert hasattr(result, 'risk_assessment')
            assert hasattr(result, 'project_alignment')
            
            # Test field types
            assert isinstance(result.project_overview, dict)
            assert isinstance(result.resource_prioritization, dict)
    
    def test_report_assembler_time_constraints_integration(self, rich_state_model):
        """Test that time constraints from profile are properly integrated.""" 
        rich_state_model.person_profile.hours_per_week = 25
        
        with patch.object(self.report_assembler, 'summary_generator') as mock_exec, \
             patch.object(self.report_assembler, 'team_analyzer') as mock_team, \
             patch.object(self.report_assembler, 'learning_synthesizer') as mock_learning, \
             patch.object(self.report_assembler, 'risk_analyzer') as mock_risk, \
             patch.object(self.report_assembler, 'goal_analyzer') as mock_goal:
            
            mock_exec.return_value = Mock(
                executive_summary="High-intensity project",
                project_scope="Ambitious development"
            )
            
            mock_team.return_value = Mock(
                role_assignments="Solo intensive development",
                collaboration_plan="Individual high-intensity work"
            )
            
            mock_learning.return_value = Mock(
                integrated_roadmap="Curated for high commitment",
                resource_prioritization='{"time-efficient": "critical"}'
            )
            
            mock_risk.return_value = Mock(
                risk_factors="High time commitment risk",
                success_criteria="Quality despite aggressive timeline",
                contingency_plans="Reduce scope if needed"
            )
            
            mock_goal.return_value = Mock(
                project_alignment="Intensive learning"
            )
            
            result = self.report_assembler.generate_report(rich_state_model)
            
            # Verify time constraints were passed to risk analyzer
            args, kwargs = mock_risk.call_args
            assert 'time_constraints' in kwargs
            assert "flexible time (20+ hours per week)" in kwargs['time_constraints']
    
    def test_report_assembler_error_handling(self, rich_state_model):
        """Test error handling when DSPy calls fail."""
        with patch.object(self.report_assembler, 'summary_generator') as mock_exec:
            # Simulate DSPy failure
            mock_exec.side_effect = Exception("LLM API failure")
            
            result = self.report_assembler.generate_report(rich_state_model)
            
            # Should return error ReportOutput
            assert isinstance(result, ReportOutput)
            assert "error" in result.executive_summary.lower()


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_report_assembler_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    assembler = ReportAssembler()
    result = assembler.generate_report(rich_state_model)
    
    assert isinstance(result, ReportOutput)
    assert result.executive_summary != ""