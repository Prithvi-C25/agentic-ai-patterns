import os
from typing import Annotated, Any, Dict, List, Optional, TypedDict

from dotenv import load_dotenv  # Load environment variables from .env file
from langchain_core.prompts import ChatPromptTemplate  # For structuring prompts

# LangChain & LangGraph components
from langchain_nebius import ChatNebius  # Nebius LLM wrapper
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch  # Tavily search tool integration
from langgraph.graph import END, StateGraph  # Build a state machine graph
from langgraph.prebuilt import ToolNode, tools_condition  # Prebuilt nodes & conditions

# Pydantic for data modeling / validation
from pydantic import BaseModel, Field

# For pretty printing output
from rich.console import Console  # Console styling
from rich.markdown import Markdown  # Render markdown in terminal

load_dotenv()  # Load environment variables from .env file

# Enable LangSmith tracing for monitoring / debugging
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = (
    "Implementing 17 Agentic Architectures"  # Project name for grouping traces
)

# Verify that all required API keys are available
for key in ["API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"]:
    if not os.environ.get(key):  # If key not found in env vars
        print(f"{key} not found. Please create a .env file and set it.")


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("DEPLOYMENT_NAME")


def get_openai_llm():
    return ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL, temperature=0)
