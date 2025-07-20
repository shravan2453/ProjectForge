import os
import dspy
from app.workflow import run_workflow
from app.state import StateModel
from app.person import PersonProfile
import dotenv

# Load environment variables
dotenv.load_dotenv()


lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=os.getenv("OPENAI_API_KEY"))
dspy.configure(lm=lm)

# Create basic state to test

def create_test_state():
    """Create a basic state model for testing."""
    # Person Profile

    profile = PersonProfile(
        user_type="student",
        experience_level="beginner",
        has_technical_background=True,
        skill_domains=["programming"],
        learning_preference="hands-on",
        hours_per_week=12
    )


    # Create statemodel
    state = StateModel(
        user_id="nati",
        session_id="test_session",
        person_profile=profile,
        project_goal="AI-Powered Eco-Tourism Route Recommendation Engine",
        interests= ["web development", "AI"],
        technical_skills= ["HTML", "CSS", "JavaScript"],
        end_goal = "Create a system that suggests eco-tourism routes based on preferences, environmental impact, and real-time conditions."
    )

    return state

if __name__ == "__main__":
       
       # Create test state
       print("Creating test state...")
       test_state = create_test_state()

       # Run the workflow
       print("running workflow...")
       result = run_workflow(test_state)
       # Print the result
       print(result)