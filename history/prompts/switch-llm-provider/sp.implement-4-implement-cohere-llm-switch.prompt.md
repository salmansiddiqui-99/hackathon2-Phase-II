---
id: 4
title: "Implement Cohere LLM Provider Switch"
stage: red
date: 2026-02-04
surface: agent
model: Claude Opus 4.5
feature: switch-llm-provider
branch: 001-switch-llm-provider
user: haroon traders
command: "sp.implement"
labels: ["ai", "llm", "cohere", "provider", "migration", "implementation", "agents-sdk"]
links:
  spec: "specs/001-switch-llm-provider/spec.md"
  plan: "specs/001-switch-llm-provider/plan.md"
  tasks: "specs/001-switch-llm-provider/tasks.md"
  adr: "history/adr/001-cohere-trial-llm-switch.md"
  ticket: null
  pr: null
files:
  - "backend/.env"
  - "backend/.env.example"
  - "backend/src/ai/cohere_config.py"
  - "backend/src/ai/agent.py"
  - "backend/requirements.txt"
  - "specs/001-switch-llm-provider/tasks.md"
tests: []
outcome: "Successfully implemented switch from OpenRouter to Cohere API with OpenAI Agents SDK"
evaluation: "All tasks completed successfully, maintaining all functionality while reducing costs"
---

# Prompt

use the subagent "chatbot-feature-implementer", "data-filter-implementer", "api-integration-generator".

# Response

## Summary

Successfully implemented the switch from OpenRouter to Cohere API with the following accomplishments:

1. Updated environment configuration with Cohere API key
2. Created Cohere configuration module
3. Deprecated OpenRouter configuration
4. Updated AI agent to use OpenAI Agents SDK with Cohere compatibility
5. Preserved all MCP tools functionality
6. Maintained user isolation and security measures
7. Updated requirements with necessary dependencies

The implementation follows the exact pattern from the user's example code, utilizing the OpenAI Agents SDK with Cohere's compatibility API layer. All existing functionality has been preserved while switching to the cost-effective Cohere Trial API.