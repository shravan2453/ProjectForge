# TODO: Implement form parsing logic using DSPy to predict project type and complexity (Chain of Thought or Predict)

from typing import Literal, TypedDict, List, Optional, Dict, Any
import asyncio
import dspy


class ClassifierOutput(BaseModel):
    project_type: str = Field(..., description="The classified project type.")
    complexity_level: str = Field(..., description="The assessed complexity level.")
    recommended_resources: List[str] = Field(..., description="List of suggested learning resources.")
    skill_gaps: str = Field(..., description="Skills the user should develop for this project.")
    reasoning: str = Field(..., description="The model's reasoning or interpretation of the user's inputs.")

class ProjectTypeClassify(dspy.Signature):

    project_purpose: str = dspy.InputField(desc="What is the project for?")
    topic_of_interest: str = dspy.InputField(desc="What topic is the user interested in?")
    potential_idea: str = dspy.InputField(desc="Does the user have a specific idea or none at all?")
    

    project_type: str = dspy.OutputField(desc="The classified project type.")

    

class ComplexityClassify(dspy.Signature):
    """Determines the complexity of a project based on user inputs."""
    technical_skills: List[str] = dspy.InputField(desc="Technical skills the user wants to apply.")
    project_type: str = dspy.InputField(desc="The determined project type.")
    additional_info: str = dspy.InputField(desc="Any additional context the user has provided.")

    project_complexity: str = dspy.OutputField(desc="Predicted project complexity.")
    reasoning: str = dspy.OutputField(desc="The model's reasoning or interpretation of the user's inputs.")


#TODO:  Later tweak the resources to also include more specific advice based on the user's experience level with the topics they wish to use

class ResourceRecommend(dspy.Signature):
    """Recommends initial resources and learning paths based on project classification."""
    
    project_type: str = dspy.InputField(desc="The classified project type.")
    project_complexity: str = dspy.InputField(desc="The assessed complexity level.")
    technical_skills: List[str] = dspy.InputField(desc="User's technical background.")
    topic_of_interest: str = dspy.InputField(desc="The subject domain.")
    additional_info: str = dspy.InputField(desc="Any extra context or requirements provided by the user.")

    recommended_resources: List[str] = dspy.OutputField(desc="List of suggested learning resources, tools, or references.")
    skill_gaps: str = dspy.OutputField(desc="Skills the user should develop for this project.")



class Classifier(dspy.Module):
    """
    Classifies the user's project based on their inputs.
    Uses a DSPy model to predict project type and complexity.
    """

    def __init__(self):
        super().__init__()
        self.type_classifier = dspy.Predict(ProjectTypeClassify)
        self.complexity_classifier = dspy.Predict(ComplexityClassify)
        self.resource_recommender = dspy.ChainOfThought(ResourceRecommend)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify the project based on user inputs.
        Returns data that matches BotState schema.
        """
        
        # Classify project type

        type_result = self.type_classifier(
            project_purpose=input_data.get("project_purpose", ""),
            topic_of_interest=input_data.get("topic_of_interest", ""),
            potential_idea=input_data.get("potential_idea", "")
        )

        # Then classify project complexity based on the type and technical skills
        complexity_result = self.complexity_classifier(
            technical_skills=input_data.get("technical_skills", ""),
            project_type=type_result.project_type,
            additional_info=input_data.get("additional_info", "")
        )

        # Reccomend resources based on the classification results
        resource_result = self.resource_recommender(
            project_type=type_result.project_type,
            project_complexity=complexity_result.project_complexity,
            technical_skills=input_data.get("technical_skills", ""),
            topic_of_interest=input_data.get("topic_of_interest", ""),
            additional_info=input_data.get("additional_info", "")
        )
        

        return ClassifierOutput(
            project_type=type_result.project_type,
            complexity_level=complexity_result.project_complexity,
            recommended_resources=resource_result.recommended_resources,
            skill_gaps=resource_result.skill_gaps,
            reasoning=complexity_result.reasoning
        )

    