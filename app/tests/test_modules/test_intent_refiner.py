"""
Test suite for the IntentRefiner DSPy module.

Tests intent clarification, idea generation, and background assessment
without making actual LLM API calls when possible.
"""

import pytest
from unittest.mock import Mock, patch
from app.modules.IntentRefiner import IntentRefiner, IntentRefinedModel
from app.state import StateModel
from app.person import PersonProfile


class TestIntentRefiner:
    """Test cases for the IntentRefiner module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.intent_refiner = IntentRefiner()
    
    def test_intent_refiner_initialization(self):
        """Test that IntentRefiner initializes correctly."""
        assert self.intent_refiner is not None
        assert hasattr(self.intent_refiner, 'intent_clarifier')
        assert hasattr(self.intent_refiner, 'idea_generator')
    
    def test_intent_refiner_output_structure(self, rich_state_model):
        """Test that IntentRefiner returns correct IntentRefinedModel structure."""
        with patch.object(self.intent_refiner, 'intent_clarifier') as mock_clarifier, \
             patch.object(self.intent_refiner, 'idea_generator') as mock_generator:
            
            # Mock clarification response
            mock_clarifier.return_value = Mock(
                clarified_intent="Build an e-commerce platform for local artisans",
                follow_up_questions=["What payment methods?", "How many vendors?"],
                suggested_project_types=["marketplace", "e-commerce", "multi-vendor"]
            )
            
            # Mock idea generation response
            mock_generator.return_value = Mock(
                generated_ideas={
                    "marketplace": ["Etsy-like platform", "Local craft marketplace"],
                    "e-commerce": ["Online store builder", "Subscription box service"]
                }
            )
            
            result = self.intent_refiner.run(rich_state_model)
            
            # Test output type
            assert isinstance(result, IntentRefinedModel)
            
            # Test all required fields exist
            assert hasattr(result, 'has_relevant_background')
            assert hasattr(result, 'background_assessment')
            assert hasattr(result, 'clarified_intent')
            assert hasattr(result, 'follow_up_questions')
            assert hasattr(result, 'suggested_project_types')
            assert hasattr(result, 'generated_ideas')
            assert hasattr(result, 'reasoning')
            
            # Test field types
            assert isinstance(result.has_relevant_background, bool)
            assert isinstance(result.background_assessment, str)
            assert isinstance(result.clarified_intent, str)
            assert isinstance(result.follow_up_questions, list)
            assert isinstance(result.suggested_project_types, list)
            assert isinstance(result.generated_ideas, list)
            assert isinstance(result.reasoning, str)
            
            # Test field values
            assert "e-commerce platform" in result.clarified_intent
            assert len(result.follow_up_questions) > 0
            assert len(result.suggested_project_types) > 0
    
    def test_intent_refiner_profile_context_usage(self, rich_state_model):
        """Test that IntentRefiner properly uses GetProfileContext data."""
        with patch.object(self.intent_refiner, 'intent_clarifier') as mock_clarifier, \
             patch.object(self.intent_refiner, 'idea_generator') as mock_generator:
            
            mock_clarifier.return_value = Mock(
                clarified_intent="Advanced web application",
                follow_up_questions=["Architecture preferences?"],
                suggested_project_types=["full-stack-app"]
            )
            
            mock_generator.return_value = Mock(
                generated_ideas={"advanced": ["Microservices app", "Real-time platform"]}
            )
            
            result = self.intent_refiner.run(rich_state_model)
            
            # Verify intent clarifier was called with profile context
            args, kwargs = mock_clarifier.call_args
            assert 'person_profile' in kwargs
            assert 'user_type' in kwargs
            assert 'experience_level' in kwargs
            assert 'skill_domains' in kwargs
            
            # Check profile data usage
            assert kwargs['user_type'] == "student"
            assert kwargs['experience_level'] == "intermediate"
            assert "programming" in kwargs['skill_domains']
    
    def test_intent_refiner_background_assessment(self, rich_state_model):
        """Test background assessment logic with technical skills."""
        # Add technical background
        rich_state_model.person_profile.has_technical_background = True
        rich_state_model.person_profile.skill_domains = ["programming", "web-development", "databases"]
        
        with patch.object(self.intent_refiner, 'intent_clarifier') as mock_clarifier, \
             patch.object(self.intent_refiner, 'idea_generator') as mock_generator:
            
            mock_clarifier.return_value = Mock(
                clarified_intent="Build a full-stack application",
                follow_up_questions=["Database preferences?"],
                suggested_project_types=["full-stack-app"]
            )
            
            mock_generator.return_value = Mock(
                generated_ideas={"full-stack": ["E-commerce platform", "Social media app"]}
            )
            
            result = self.intent_refiner.run(rich_state_model)
            
            # Test background assessment
            assert result.has_relevant_background == True
            assert "relevant" in result.background_assessment.lower()
            assert "programming" in result.background_assessment


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_intent_refiner_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    intent_refiner = IntentRefiner()
    result = intent_refiner.run(rich_state_model)
    
    assert isinstance(result, IntentRefinedModel)
    assert result.clarified_intent != ""
    assert len(result.generated_ideas) > 0
    assert isinstance(result.has_relevant_background, bool)