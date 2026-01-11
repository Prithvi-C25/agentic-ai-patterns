import sys
from pathlib import Path
from typing import List, TypedDict

from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown

# Add parent directory to path to import tools
sys.path.append(str(Path(__file__).parent.parent))
from tools import get_openai_llm

llm = get_openai_llm()

# Initialize console for pretty printing
console = Console()

print("OpenAI LLM and Console are initialized.")


class Plan(BaseModel):
    """A plan of tool calls to execute to answer the user's query."""

    steps: List[str] = Field(
        description="A list of tool calls that, when executed, will answer the user's query."
    )

class PlanningState(TypedDict):
    

def pev_planner_node(state):
    """Plans the steps needed to fulfill the user request."""
    console.print(Markdown("--- 1. Planning Steps ---"))
    planner_llm = llm.with_structured_output(DraftCode)

    prompt = f"""
    You are an expert planner. Break down the following user request into a series of actionable steps.
    
    Request: {state['user_request']}
    """

    plan = planner_llm.invoke(prompt)
    return {"plan": plan.model_dump()}
    return {"plan": plan.model_dump()}
    return {"plan": plan.model_dump()}