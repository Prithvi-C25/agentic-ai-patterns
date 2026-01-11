"""Getting started with mlflow tracking"""

import sys
from pathlib import Path
from typing import Literal

import mlflow
from langchain_core.messages import AIMessage, ToolCall
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

sys.path.append(str(Path(__file__).parent.parent))
from tools import get_openai_llm

mlflow.langchain.autolog()

mlflow.set_experiment("LangChain")
mlflow.set_tracking_uri("http://localhost:5000")


@tool
def get_weather(city: Literal["New York", "San Francisco", "Los Angeles"]) -> str:
    """Get the current weather in a city."""
    if city == "New York":
        return "It might be cloudy in nyc"
    elif city == "San Francisco":
        return "It's always sunny in sf"
    elif city == "Los Angeles":
        return "It's sunny and warm in la"


llm = get_openai_llm()

graph = create_react_agent(llm, [get_weather])

result = graph.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in San Francisco?"}]}
)
# print("Final Answer:", result)


"""Token usage tracking"""

# Get the trace object just created
last_trace_id = mlflow.get_last_active_trace_id()
trace = mlflow.get_trace(last_trace_id)

# Print the token usage:
total_usage = trace.info.token_usage
print("==Tool token usage:==")
print(f"   Input tokens: {total_usage['input_tokens']}")
print(f"   Output tokens: {total_usage['output_tokens']}")
print(f"   Total tokens: {total_usage['total_tokens']}")

# Print the token usage for each LLM call
print("\n==LLM calls token usage:==")
for span in trace.data.spans:
    if usage := span.get_attribute("mlflow.chat.tokenUsage"):
        print(f"LLM Call - {span.name}:")
        print(f"   Input tokens: {usage['input_tokens']}")
        print(f"   Output tokens: {usage['output_tokens']}")
        print(f"   Total tokens: {usage['total_tokens']}")
