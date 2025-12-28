import sys
from pathlib import Path
from typing import Dict, Optional, TypedDict

from langgraph.graph import END, StateGraph
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

sys.path.append(str(Path(__file__).parent.parent))
from reflection.nodes import critic_node, generator_node, reviser_node


class ReflectionState(TypedDict):
    """Represents the state of our reflection graph"""

    user_request: str
    draft: Optional[Dict]
    critique: Optional[Dict]
    revised_code: Optional[Dict]


print("ReflectionState TypedDict defined.")

graph_builder = StateGraph(ReflectionState)

# Add the nodes to the graph
graph_builder.add_node("generator", generator_node)
graph_builder.add_node("critic", critic_node)
graph_builder.add_node("reviser", reviser_node)

# Define the workflow edges
graph_builder.set_entry_point("generator")
graph_builder.add_edge("generator", "critic")
graph_builder.add_edge("critic", "reviser")
graph_builder.add_edge("reviser", END)

# Compile the graph
reflection_app = graph_builder.compile()
print("Reflection graph compiled successfully!")

# Visualize the graph
try:
    png_image = reflection_app.get_graph().draw_png()
    output_path = Path(__file__).parent / "reflection_app.png"
    with open(output_path, "wb") as f:
        f.write(png_image)
    print(f"Graph saved as {output_path}")
except Exception as e:
    print("Graph visualization failed:", e)


# Running the Full Workflow
user_request = "Write a Python function to find the nth Fibonacci number."
initial_input = {"user_request": user_request}

console = Console()

console.print(
    f"[bold cyan]🚀 Kicking off Reflection workflow for request:[/bold cyan] '{user_request}'\n"
)

final_state = None
for state_update in reflection_app.stream(initial_input, stream_mode="values"):
    final_state = state_update
    console.print("\n[bold green]✅ Reflection workflow complete![/bold green]")


# Analyzing Initial and Final Output
if (
    final_state
    and "draft" in final_state
    and "critique" in final_state
    and "revised_code" in final_state
):
    console.print(Markdown("### Initial Draft Code:"))
    console.print(Markdown(f"**Explanation:** {final_state['draft']['explanation']}"))
    # Use rich's Syntax for proper code highlighting
    console.print(
        Syntax(
            final_state["draft"]["code"], "python", theme="monokai", line_numbers=True
        )
    )

    console.print(Markdown("### Critique:"))
    console.print(
        Markdown(f"**Summary:** {final_state['critique']['critique_summary']}")
    )
    console.print(Markdown("**Suggested Improvements:**"))
    for suggestion in final_state["critique"]["suggested_improvement"]:
        console.print(Markdown(f"- {suggestion}"))

    console.print(Markdown("### Revised Code:"))
    console.print(
        Markdown(
            f"**Revision Explanation:** {final_state['revised_code']['revised_explanation']}"
        )
    )
    console.print(
        Syntax(
            final_state["revised_code"]["revised_code"],
            "python",
            theme="monokai",
            line_numbers=True,
        )
    )

else:
    console.print(
        """[bold red]Error: The `final_state` is not available or is incomplete. \n
        Please check the execution of the previous cells.[/bold red]"""
    )
