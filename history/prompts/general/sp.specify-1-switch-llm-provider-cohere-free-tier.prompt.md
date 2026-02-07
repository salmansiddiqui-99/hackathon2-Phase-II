---
id: 1
title: "Switch LLM Provider from OpenRouter to Cohere Free Tier"
stage: spec
date: 2026-02-04
surface: agent
model: Claude Opus 4.5
feature: switch-llm-provider
branch: 001-switch-llm-provider
user: haroon traders
command: /sp.specify Phase III Extension: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)
labels: ["ai", "llm", "cohere", "provider", "migration", "specification"]
links:
  spec: "specs/001-switch-llm-provider/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-switch-llm-provider/spec.md"
  - "specs/001-switch-llm-provider/checklists/requirements.md"
tests: []
outcome: "Successfully created feature specification for switching from OpenRouter to Cohere's free trial tier while preserving all Phase III functionality."
evaluation: "Specification meets all requirements with clear user stories, functional requirements, and success criteria."
---

# Prompt

Phase III Extension: Switch LLM Provider from OpenRouter to Cohere (Free Trial Tier)

Target audience: Hackathon participants and judges evaluating flexibility in AI provider integration and cost-optimization strategies
Focus: Replace the OpenRouter-based LLM configuration (DeepSeek model) with Cohere's free Trial API key using the OpenAI-compatible Compatibility API layer, while preserving all Phase III functionality (MCP tools, stateless chat endpoint, agent behavior, ChatKit integration)

Success criteria:
- All LLM inference calls now route through Cohere's Compatibility API (OpenAI SDK compatible)
- Configuration uses provided Cohere Trial API key: SqnhRaifcIHJyGeTqODA955lm5VvIlP1cJHYtDmM
- Base URL set to Cohere's compatibility endpoint: https://api.cohere.com/v1 (or exact compatibility base as per latest docs)
- Use a strong free-tier-compatible chat model from Cohere's Command family, preferably:
  - command-r (if available in trial)
  - command-r-plus (if trial allows)
  - command-r7b (smaller/faster variant often more permissive in trial limits)
  - fallback to the most capable model explicitly allowed under trial restrictions
- Agent still uses OpenAI Agents SDK → configured with AsyncOpenAI client pointing to Cohere compatibility endpoint
- No change to MCP tools, database models, chat endpoint signature, or agent behavior rules
- Maintains exact natural language understanding and tool-calling behavior for Basic Level todo operations
- Trial usage constraints acknowledged (rate limits ~20 req/min chat, ~1,000 calls/month total – suitable for demo/hackathon testing)
- All code remains generated via Claude Code; no manual edits

Constraints:
- Must use Cohere **Trial** key only (free, evaluation/non-production)
- Cannot use paid/production Cohere keys or assume unlimited usage
- Keep OpenAI Agents SDK compatibility layer (AsyncOpenAI client + base_url override)
- Do NOT switch to native Cohere Python SDK unless Compatibility API fails – prefer OpenAI-style integration for minimal code changes
- Respect trial rate limits in demo (avoid high-frequency calls in video)
- No degradation of Phase III success criteria (multi-turn context, tool calling, user isolation)

Not building:
- Native Cohere SDK migration (cohere.ClientV2 / co.chat)
- Paid Cohere features or production-tier models
- New models outside Cohere's Command family
- Changes to Intermediate/Advanced features (still Basic Level only in Phase III)
- Reverting to direct OpenAI or other providers

Implementation guidance / rationale:
- Use pattern similar to provided example (AsyncOpenAI with custom base_url + api_key)
- Expected minimal change: replace base_url and api_key + select Cohere model name
- Document in CLAUDE.md or README why Cohere Trial was chosen (free vs. OpenRouter paid tiers)

This spec allows seamless provider swap while staying within hackathon constraints and leveraging Cohere's free trial for cost-free inference during development and demo.

# Response

I'll now create a feature specification for switching the LLM provider from OpenRouter to Cohere. Let me start by determining a short name and checking for existing branches.

The feature is about switching LLM providers from OpenRouter to Cohere's free trial tier, so a good short name would be "switch-llm-provider".

Now let me check for existing branches and create a new feature:

...

[The response contains the full interaction of creating the feature specification]