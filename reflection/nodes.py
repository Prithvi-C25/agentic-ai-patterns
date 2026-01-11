import json
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

# Add parent directory to path to import tools
sys.path.append(str(Path(__file__).parent.parent))
from reflection.schema import Critique, DraftCode, RevisedCode
from tools import get_openai_llm

llm = get_openai_llm()

# Initialize console for pretty printing
console = Console()

print("OpenAI LLM and Console are initialized.")


def generator_node(state):
    """Generates initial code draft based on user request."""
    console.print(Markdown("--- 1. Generating Initial Draft ---"))
    generator_llm = llm.with_structured_output(DraftCode)

    prompt = f"""
    You are an expert Python programmer. Write a Python function to solve the following request.
    Provide a simple, clear implementation and an explanation.
    
    Request: {state['user_request']}
    """

    draft = generator_llm.invoke(prompt)
    return {"draft": draft.model_dump()}


def critic_node(state):
    """Critiques the generated code draft for potential improvements."""
    console.print(Markdown("--- 2. Critiquing the Draft ---"))
    critic_llm = llm.with_structured_output(Critique)

    code_to_critique = state["draft"]["code"]

    prompt = f"""
    You are an expert code reviewer and senior Python developer. Your task is to perform a thorough critique of the following code.
    
    Analyze the code for:
    1.  **Bugs and Errors:** Are there any potential runtime errors, logical flaws, or edge cases that are not handled?
    2.  **Efficiency and Best Practices:** Is this the most efficient way to solve the problem? Does it follow standard Python conventions (PEP 8)?
    
    Provide a structured critique with specific, actionable suggestions.
    
    Code to Review:
    ```python
    {code_to_critique}
    """

    critique = critic_llm.invoke(prompt)
    return {"critique": critique.model_dump()}


def reviser_node(state):
    """Revises the code draft based on the critique provided."""
    console.print(Markdown("--- 3. Revising the Code ---"))
    reviser_llm = llm.with_structured_output(RevisedCode)

    draft_code = state["draft"]["code"]
    critique_summary = json.dumps(state["critique"], indent=2)

    # suggestions = "\n".join(state["critique"]["suggested_improvement"])

    prompt = f"""
    You are an expert Python programmer tasked with refining a piece of code based on a critique.
    
    Your goal is to rewrite the original code, implementing all the suggested improvements from the critique.
    
    **Original Code:**
    ```python
    {draft_code}
    ```

    **Critique and Summary:**
    {critique_summary}
    
    Please provide the final, refined code and a summary of the changes you made.
    """

    revised_code = reviser_llm.invoke(prompt)
    return {"revised_code": revised_code.model_dump()}
