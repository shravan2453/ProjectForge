"""
Test suite for the Classifier DSPy module.

Tests basic functionality, output structure, and different input scenarios
without making actual LLM API calls when possible.
"""

import pytest
from unittest.mock import Mock, patch
from app.modules.Classifier import Classifier, ClassifierOutput
from app.state import StateModel
from app.person import PersonProfile


class TestClassifier:
    """Test cases for the Classifier module."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.classifier = Classifier()
    
    def test_classifier_initialization(self):
        """Test that Classifier initializes correctly."""
        assert self.classifier is not None
        assert hasattr(self.classifier, 'type_classifier')
        assert hasattr(self.classifier, 'complexity_classifier')
        assert hasattr(self.classifier, 'resource_recommender')
    
    def test_classifier_output_structure(self, rich_state_model):
        """Test that Classifier returns correct ClassifierOutput structure."""
        # Mock the DSPy calls to avoid API requests
        with patch.object(self.classifier, 'type_classifier') as mock_type, \
             patch.object(self.classifier, 'complexity_classifier') as mock_complexity, \
             patch.object(self.classifier, 'resource_recommender') as mock_resources:
            
            # Mock responses
            mock_type.return_value = Mock(
                project_type="web-app",
                project_subtype="full-stack",
                suitable_for_portfolio=True
            )
            
            mock_complexity.return_value = Mock(
                project_complexity="intermediate",
                complexity_reasoning="Good match for user's skill level",
                skill_alignment_score="high",
                learning_curve_assessment="moderate learning curve",
                reasoning="Well-balanced project complexity"
            )
            
            mock_resources.return_value = Mock(
                recommended_resources=["React docs", "Node.js tutorial"],
                skill_gaps="Frontend state management"
            )
            
            # Run classifier
            result = self.classifier.run(rich_state_model)
            
            # Test output type
            assert isinstance(result, ClassifierOutput)
            
            # Test all required fields exist
            assert hasattr(result, 'project_type')
            assert hasattr(result, 'complexity_level')
            assert hasattr(result, 'complexity_reasoning')
            assert hasattr(result, 'skill_alignment_score')
            assert hasattr(result, 'learning_curve_assessment')
            assert hasattr(result, 'recommended_resources')
            assert hasattr(result, 'skill_gaps')
            assert hasattr(result, 'reasoning')
            
            # Test field types
            assert isinstance(result.project_type, str)
            assert isinstance(result.complexity_level, str)
            assert isinstance(result.complexity_reasoning, str)
            assert isinstance(result.skill_alignment_score, str)
            assert isinstance(result.learning_curve_assessment, str)
            assert isinstance(result.recommended_resources, list)
            assert isinstance(result.skill_gaps, str)
            assert isinstance(result.reasoning, str)
            
            # Test field values
            assert result.project_type == "web-app"
            assert result.complexity_level == "intermediate"
            assert len(result.recommended_resources) > 0
            
    def test_classifier_with_minimal_state(self, minimal_state_model):
        """Test Classifier with minimal StateModel data."""
        # Add required fields for classification
        minimal_state_model.project_goal = "Build a simple website"
        minimal_state_model.interests = ["web development"]
        minimal_state_model.end_goal = "Learn programming"
        
        # Add a basic person profile
        minimal_state_model.person_profile = PersonProfile(
            user_type="student",
            experience_level="beginner",
            has_technical_background=False,
            skill_domains=["basic-programming"]
        )
        
        with patch.object(self.classifier, 'type_classifier') as mock_type, \
             patch.object(self.classifier, 'complexity_classifier') as mock_complexity, \
             patch.object(self.classifier, 'resource_recommender') as mock_resources:
            
            # Mock simple responses
            mock_type.return_value = Mock(
                project_type="static-website",
                project_subtype="personal-site",
                suitable_for_portfolio=True
            )
            
            mock_complexity.return_value = Mock(
                project_complexity="beginner",
                complexity_reasoning="Perfect for learning basics",
                skill_alignment_score="medium",
                learning_curve_assessment="gentle learning curve",
                reasoning="Good starter project"
            )
            
            mock_resources.return_value = Mock(
                recommended_resources=["HTML/CSS basics", "Web development fundamentals"],
                skill_gaps="HTML, CSS, basic JavaScript"
            )
            
            result = self.classifier.run(minimal_state_model)
            
            assert isinstance(result, ClassifierOutput)
            assert result.project_type == "static-website"
            assert result.complexity_level == "beginner"
            assert "HTML" in result.skill_gaps
    
    def test_classifier_intent_refinement_needed(self):
        """Test Classifier when intent refinement is needed."""
        # Create state with insufficient information
        insufficient_state = StateModel(
            user_id="test_user",
            session_id="test_session",
            # Missing: project_goal, interests, end_goal
        )
        
        result = self.classifier.run(insufficient_state)
        
        assert isinstance(result, ClassifierOutput)
        assert result.project_type == "needs_refinement"
        assert result.complexity_level == "unknown"
        assert "Intent refinement required" in result.recommended_resources
        assert result.skill_gaps == "Insufficient information"
        assert "Insufficient information provided" in result.reasoning
        
        # Check that intent refinement flags are set
        assert insufficient_state.intent_refinement_needed == True
        assert len(insufficient_state.refinement_hints) > 0
    
    def test_classifier_with_past_projects(self, rich_state_model):
        """Test Classifier considers past projects for personalization."""
        # Add completed tasks to state
        rich_state_model.completed_tasks = [
            {
                "project_type": "web-app",
                "status": "completed",
                "technologies": ["React", "Node.js"],
                "outcome": "Successfully deployed blog"
            },
            {
                "project_type": "data-analysis",
                "status": "completed", 
                "technologies": ["Python", "Pandas"],
                "outcome": "Created visualization dashboard"
            }
        ]
        
        with patch.object(self.classifier, 'type_classifier') as mock_type, \
             patch.object(self.classifier, 'complexity_classifier') as mock_complexity, \
             patch.object(self.classifier, 'resource_recommender') as mock_resources:
            
            mock_type.return_value = Mock(
                project_type="full-stack-app",
                project_subtype="advanced-web-app",
                suitable_for_portfolio=True
            )
            
            mock_complexity.return_value = Mock(
                project_complexity="intermediate-advanced",
                complexity_reasoning="User has proven track record with similar projects",
                skill_alignment_score="high",
                learning_curve_assessment="manageable - building on existing skills",
                reasoning="Good progression from previous projects"
            )
            
            mock_resources.return_value = Mock(
                recommended_resources=["Advanced React patterns", "System design"],
                skill_gaps="Advanced architecture patterns"
            )
            
            result = self.classifier.run(rich_state_model)
            
            # Verify the complexity classifier was called with past projects context
            args, kwargs = mock_complexity.call_args
            assert 'past_projects_context' in kwargs
            past_projects_arg = kwargs['past_projects_context']
            assert "completed 2 previous projects" in past_projects_arg.lower()
            assert "web-app" in past_projects_arg
            assert "data-analysis" in past_projects_arg
    
    def test_classifier_profile_context_usage(self, rich_state_model):
        """Test that Classifier properly uses GetProfileContext data."""
        with patch.object(self.classifier, 'type_classifier') as mock_type, \
             patch.object(self.classifier, 'complexity_classifier') as mock_complexity, \
             patch.object(self.classifier, 'resource_recommender') as mock_resources:
            
            # Mock responses
            mock_type.return_value = Mock(
                project_type="web-app",
                project_subtype="full-stack",
                suitable_for_portfolio=True
            )
            
            mock_complexity.return_value = Mock(
                project_complexity="intermediate",
                complexity_reasoning="Appropriate for user's experience level",
                skill_alignment_score="high",
                learning_curve_assessment="moderate",
                reasoning="Good skill match"
            )
            
            mock_resources.return_value = Mock(
                recommended_resources=["React docs"],
                skill_gaps="State management"
            )
            
            result = self.classifier.run(rich_state_model)
            
            # Verify complexity classifier was called with profile data
            args, kwargs = mock_complexity.call_args
            assert 'user_experience_level' in kwargs
            assert 'user_type' in kwargs
            assert 'user_skills' in kwargs
            
            # Check that profile context is used
            assert kwargs['user_experience_level'] == "intermediate"
            assert kwargs['user_type'] == "student"  # From rich_state_model fixture
            assert "programming" in kwargs['user_skills']  # From skill_domains
    
    def test_classifier_output_validation(self, rich_state_model):
        """Test that ClassifierOutput validates its fields correctly."""
        with patch.object(self.classifier, 'type_classifier') as mock_type, \
             patch.object(self.classifier, 'complexity_classifier') as mock_complexity, \
             patch.object(self.classifier, 'resource_recommender') as mock_resources:
            
            mock_type.return_value = Mock(project_type="web-app")
            mock_complexity.return_value = Mock(
                project_complexity="intermediate",
                complexity_reasoning="Test reasoning",
                skill_alignment_score="high", 
                learning_curve_assessment="moderate",
                reasoning="Overall reasoning"
            )
            mock_resources.return_value = Mock(
                recommended_resources=["Resource 1", "Resource 2"],
                skill_gaps="Gap analysis"
            )
            
            result = self.classifier.run(rich_state_model)
            
            # Test that we can serialize/deserialize (Pydantic validation)
            result_dict = result.model_dump()
            assert 'project_type' in result_dict
            assert 'complexity_level' in result_dict
            assert 'recommended_resources' in result_dict
            
            # Test that we can recreate from dict
            recreated = ClassifierOutput(**result_dict)
            assert recreated.project_type == result.project_type
            assert recreated.complexity_level == result.complexity_level


# Integration test (optional - for when you want to test with real DSPy)
@pytest.mark.skip(reason="Requires actual DSPy/LLM setup - enable when ready for integration testing")
def test_classifier_integration_real_dspy(rich_state_model):
    """Integration test with real DSPy calls (requires API keys)."""
    classifier = Classifier()
    result = classifier.run(rich_state_model)
    assert result