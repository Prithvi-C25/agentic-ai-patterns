import sys
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

sys.path.append(str(Path(__file__).parent.parent))
from reflection.nodes import (
    pev_executor_node,
    pev_planner_node,
    synthesizer_node,
    verifier_node,
)


class PEVState(TypedDict):
    """Represents the state of our Planner-Executer-Verifier graph"""

    user_request: str
    plan: Optional[List[str]]
    last_tool_result: Optional[str]
    intermediate_steps: List[str]
    final_answer: Optional[str]


def pev_router(state: PEVState):
    """Routes execution based on verification and plan status."""

    if not state["plan"]:
        # Check if the plan is empty because the verification failed
        if state["intermediate_steps"] and (
            "Verification Failed" in state["intermediate_steps"][-1]
        ):
            console.print("--- ROUTER: Verification failed. Re-planning... ---")
            return "plan"  # Re-plan if verification failed
        else:
            console.print("--- ROUTER: plan complete. Moving to synthesis... ---")
            return "synthesize"  # Move to synthesis if no plan exists

    else:
        console.print(
            "--- ROUTER: Plan has more steps. Continuing with execution... ---"
        )
        return "execute"  # Continue executing the plan


pev_graph_builder = StateGraph(PEVState)

# Add the nodes to the graph
pev_graph_builder.add_node("plan", pev_planner_node)
pev_graph_builder.add_node("execute", pev_executor_node)
pev_graph_builder.add_node("verify", verifier_node)
pev_graph_builder.add_node("synthesize", synthesizer_node)

# Define the workflow edges
pev_graph_builder.set_entry_point("plan")
pev_graph_builder.add_edge("plan", "execute")
pev_graph_builder.add_edge("execute", "verify")
pev_graph_builder.add_edge("verify", pev_router)

pev_graph_builder.add_edge("synthesize", END)


# Compile the graph
pev_agent_app = pev_graph_builder.compile()
print("Planner-Executor-Verifier graph compiled successfully!")

# Visualize the graph
try:
    png_image = pev_agent_app.get_graph().draw_png()
    output_path = Path(__file__).parent / "pev_agent_app.png"
    with open(output_path, "wb") as f:
        f.write(png_image)
    print(f"Graph saved as {output_path}")
except Exception as e:
    print("Graph visualization failed:", e)


# # Running the Full Workflow
# user_request = "Write a Python function to find the nth Fibonacci number."
# initial_input = {"user_request": user_request}

# console = Console()

# console.print(
#     f"[bold cyan]🚀 Kicking off Reflection workflow for request:[/bold cyan] '{user_request}'\n"
# )

# final_state = None
# for state_update in reflection_app.stream(initial_input, stream_mode="values"):
#     final_state = state_update
#     console.print("\n[bold green]✅ Reflection workflow complete![/bold green]")


# # Analyzing Initial and Final Output
# if (
#     final_state
#     and "draft" in final_state
#     and "critique" in final_state
#     and "revised_code" in final_state
# ):
#     console.print(Markdown("### Initial Draft Code:"))
#     console.print(Markdown(f"**Explanation:** {final_state['draft']['explanation']}"))
#     # Use rich's Syntax for proper code highlighting
#     console.print(
#         Syntax(
#             final_state["draft"]["code"], "python", theme="monokai", line_numbers=True
#         )
#     )

#     console.print(Markdown("### Critique:"))
#     console.print(
#         Markdown(f"**Summary:** {final_state['critique']['critique_summary']}")
#     )
#     console.print(Markdown("**Suggested Improvements:**"))
#     for suggestion in final_state["critique"]["suggested_improvement"]:
#         console.print(Markdown(f"- {suggestion}"))

#     console.print(Markdown("### Revised Code:"))
#     console.print(
#         Markdown(
#             f"**Revision Explanation:** {final_state['revised_code']['revised_explanation']}"
#         )
#     )
#     console.print(
#         Syntax(
#             final_state["revised_code"]["revised_code"],
#             "python",
#             theme="monokai",
#             line_numbers=True,
#         )
#     )

# else:
#     console.print(
#         """[bold red]Error: The `final_state` is not available or is incomplete. \n
#         Please check the execution of the previous cells.[/bold red]"""
#     )
# else:
#     console.print(
#         """[bold red]Error: The `final_state` is not available or is incomplete. \n
#         Please check the execution of the previous cells.[/bold red]"""
#     )
