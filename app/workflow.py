import dspy 
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import StateModel
from app.nodes.BackgroundNode import background_assesor_node
from app.nodes.ClassifyNode import classify_node  
from app.nodes.IntentRefinerNode import intent_refiner_node                                  
from app.nodes.MilestoneNode import milestone_node                                          
from app.nodes.TimelineNode import timeline_node                                            
from app.nodes.ReportNode import report_node
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


def create_workflow():
    """
    Create the LangGraph workflow for project planning.
    This function initializes the state graph and adds nodes to it.
    """
    
    workflow = StateGraph(StateModel)  # Initialize the state graph with the StateModel
   

    workflow.add_node("BackgroundAssessor", background_assesor_node)
    workflow.add_node("Classifier", classify_node)
    workflow.add_node("MilestoneGenerator", milestone_node)
    workflow.add_node("TimelineScheduler", timeline_node)
    workflow.add_node("ReportAssembler", report_node)

    # Connect them in sequence
    workflow.add_edge(START, "BackgroundAssessor")
    workflow.add_edge("BackgroundAssessor", "Classifier")
    workflow.add_edge("Classifier", "MilestoneGenerator")
    workflow.add_edge("MilestoneGenerator", "TimelineScheduler")
    workflow.add_edge("TimelineScheduler", "ReportAssembler")
    workflow.add_edge("ReportAssembler", END)
    return workflow.compile()  # Compile the workflow to finalize it

# Create the workflow

simple_workflow = create_workflow()


def run_workflow(state: StateModel) -> StateModel:
    """
    Run the LangGraph workflow with the initial state."""

    
    # Run the workflow with the initial state
    result = simple_workflow.invoke(state)

    return StateModel(**result)  # Return the final state after processing