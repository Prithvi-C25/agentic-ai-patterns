# Agentic Architectures 1: Reflection

## Definition

The Reflection architecture involves an agent critiquing and revising its own output before returning a final answer. Instead of a single-pass generation, it engages in a multi-step internal monologue: produce, evaluate, and improve. This mimics the human process of drafting, reviewing, and editing to catch errors and enhance quality.

## High-level Workflow

Generate: The agent produces an initial draft or solution based on the user's prompt.
Critique: The agent then switches roles to become a critic. It asks itself questions like: "What could be wrong with this answer?", "What is missing?", "Is this solution optimal?", or "Are there any logical flaws or bugs?".
Refine: Using the insights from its self-critique, the agent generates a final, improved version of the output.

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