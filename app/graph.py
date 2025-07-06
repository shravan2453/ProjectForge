#LangGraph wiring
import os
import getpass
import json
# Ensure you have the necessary packages installed:

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import ToolMessage, AIMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver 


load_dotenv()  # Load environment variables from .env file if it exists
