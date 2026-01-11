# Agentic Architectures 1: PEV (Planner-Executor-Verifier)

## Definition

Our Planning agent works well when the path is clear, it makes a plan and follows it. But there’s a hidden assumption ...

What happens when things go wrong? If a tool fails, an API is down, or search returns junk, a standard planner just passes the error along, ending in failure or nonsense. PEV is important for building robust and reliable workflows. You do use it anywhere an agent interacts with external tools that might be unreliable.

## High-level Workflow

PEV (Planner-Executor-Verifier) architecture is a simple but powerful upgrade to the Planning pattern that adds a critical layer of quality control and self-correction.

1. Plan: A ‘Planner’ agent creates a sequence of steps.
2. Execute: An ‘Executor’ agent takes the next step from the plan and calls the tool.
3. Verify: A ‘Verifier’ agent examines the tool’s output. It checks for correctness, relevance, and errors.
4. Route & Iterate: Based on the Verifier’s judgment:

If the step succeeded, the agent moves to the next step in the plan.
If the step failed, the agent loops back to the Planner to create a new plan, now aware of the failure.
If the plan is complete, it proceeds to the end.

## When to Use / Applications

Code Generation: The initial code might have bugs, be inefficient, or lack comments. Reflection allows the agent to act as its own code reviewer, catching errors and improving style before presenting the final script.
Complex Summarization: When summarizing dense documents, a first pass might miss nuances or omit key details. A reflection step helps ensure the summary is comprehensive and accurate.
Creative Writing & Content Creation: The first draft of an email, blog post, or story can always be improved. Reflection allows the agent to refine its tone, clarity, and impact.

## Strengths & Weaknesses

### Strengths:

Improved Quality: Directly addresses and corrects errors, leading to more accurate, robust, and well-reasoned outputs.
Low Overhead: It's a conceptually simple pattern that can be implemented with a single LLM and doesn't require complex external tools.

### Weaknesses:

Self-Bias: The agent is still limited by its own knowledge and biases. If it doesn't know a better way to solve a problem, it can't critique its way to a better solution. It can fix flaws it recognizes but can't invent knowledge it lacks.
Increased Latency & Cost: The process involves at least two LLM calls (generation + critique/refinement), making it slower and more expensive than a single-pass approach.