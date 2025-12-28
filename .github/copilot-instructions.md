---
applyTo: "**/*.py"
---

# Project coding standards for Python
1. Virtual Environments with uv:
  - Always use 'uv sync' for creating virtual environments in Python projects.
  - When prompted to include a new dependency, ensure it is added to the pyproject.toml file and then update the virtual env with 'uv lock' and using 'uv sync'.

2. Apply best-practice design patterns (e.g., DRY, SOLID).
- Always prioritize readability and clarity.
- Follow Follow the PEP 8 style guide for Python or language/framework-specific best practices
Use Version Control:

3. Unit Testing:
Always use pytest modules for unit testing. Add unit tests for functions and modules, especially in large or long-lived projects. Follow Best Practices:

4. Write clear and concise comments for each function. Use type hints for function arguments, variables, and return values. Ensure functions have descriptive names.

5. Do not expose applications to the public internet by default.
Implement authentication and authorization for public applications.
Vulnerability Analysis:

6. End-to-End Testing:
- While creating and prototyping large scale projects, create end-to-end tests using pytest and follow best practises based on the chosen tool framework (Ex: PyTorch, Langchain).

7. Only after the final step, Add Documentation:
All classes and functions must include docstrings.
Projects must include a README.md file.
Projects must specify dependency versions (e.g., with a lock file).

## Optional Rules
11. Azure Rules:
Use Azure Tools: When handling requests related to Azure, always use your tools.
Use Azure Code Gen Best Practices: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `bestpractices` tool if available. Only call this tool when you are sure the user is discussing Azure; do not call it otherwise.
Use Azure Deployment Best Practices: When deploying to Azure or preparing applications for deployment to Azure, invoke your `bestpractices` tool if available. Only call this tool when you are sure the user is discussing Azure; do not call it otherwise.
Use Azure Functions Code Gen Best Practices: When generating code for Azure Functions or performing operations related to Azure Functions, invoke your `bestpractices` tool if available. Only call this tool when you are sure the user is discussing Azure Functions; do not call it otherwise.
Use Azure Functions Deployment Best Practices: When deploying Azure Functions apps to Azure or preparing for the deployment, invoke your `bestpractices` tool if available. Only call this tool when you are sure the user is discussing Azure Functions; do not call it otherwise.
Use Azure SWA Best Practices: When working with static web apps, invoke your `bestpractices` tool if available. Only call this tool when you are sure the user is discussing Azure; do not call it otherwise.
Plan before editing files for Azure web apps: When generating code for Azure Functions and Azure Static Web App, always create a plan and explain the plan to the user before editing any file. Proceed with editing the files after getting consent from the user.
Summarize topic before taking action: When the user asks for something about Azure, invoke the azure_development-summarize_topic tool once to discover potential recommended configurations.