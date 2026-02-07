---
id: "PHR-0002"
title: "Create Implementation Plan Natural Task Ref By Title"
stage: "plan"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "natural-task-reference-by-title"
branch: "5-natural-task-reference-by-title"
user: "haroon traders"
command: "manual"
labels: ["plan", "task-management", "natural-language", "chatbot"]
links:
  spec: "specs/5-natural-task-reference-by-title/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/5-natural-task-reference-by-title/plan.md"
  - "specs/5-natural-task-reference-by-title/research.md"
  - "specs/5-natural-task-reference-by-title/data-model.md"
  - "specs/5-natural-task-reference-by-title/quickstart.md"
  - "specs/5-natural-task-reference-by-title/contracts/title-resolution-api.yaml"
  - "history/prompts/natural-task-reference-by-title/phr-0002-create-implementation-plan-natural-task-ref-by-title.prompt.md"
tests: []
---

# Prompt History Record: Create Implementation Plan Natural Task Ref By Title

## Prompt Text

**Phase III Extension: Natural Task Reference by Title (No Task ID Prompting)**

```yaml
create:
  - system_prompt_major_upgrade: Rewrite agent instructions to forbid asking for task IDs
  - title_based_reasoning_guidelines: Add detailed few-shot examples and rules for title → task_id resolution
  - internal_task_resolution_logic: Instruct agent to (when needed):
    - Call list_tasks internally first
    - Match user-provided title against returned task titles (fuzzy/partial/case-insensitive)
    - If unique match → proceed with tool call using found task_id
    - If multiple matches → respond with numbered list of matching titles (no IDs shown) and ask for clarification
    - If no match → respond helpfully + optionally list recent/open tasks
  - clarification_response_format: Define clean, natural disambiguation message template
  - confirmation_messages_update: Ensure all success/error confirmations use title, not ID

decisions_needing_documentation:
  - title_matching_strategy:
      chosen: LLM-driven fuzzy/partial matching via prompt reasoning
      rationale: Most natural, no extra code, leverages Cohere's strong reasoning
  - disambiguation_threshold:
      chosen: ≥2 similar titles → trigger clarification
      rationale: Balances precision vs. over-asking
  - list_tasks_calling_frequency:
      chosen: Only when title-based command detected and no exact cached context
      rationale: Minimizes unnecessary tool calls (rate-limit friendly)
  - user_exposed_information:
      chosen: Show only titles (never internal IDs) during clarification
      rationale: Keeps UX human-like and non-technical

testing_strategy:
  - validation_checks:
      - "complete buy groceries" → finds & completes task titled "buy groceries" (no ID asked)
      - "delete finish report" → deletes correct task by title
      - "update morning run to evening walk" → updates task
      - Two tasks named "buy milk" → bot replies:
        "I found two tasks called 'buy milk':
        1. buy milk (created today)
        2. buy milk for party
        Which one do you mean?"
      - Reply "the second one" or "for party" → proceeds correctly
      - "mark invalid title as done" → "I couldn't find a task called 'invalid title'. Here are your tasks: …"
  - method: Multi-turn ChatKit session in demo video showing:
    - Single-title commands (silent success)
    - Ambiguous case + clarification + resolution
    - Non-existent title handling

technical_details:
  - approach: 100% prompt engineering + few-shot examples (zero code change preferred)
  - fallback_if_prompt_insufficient: Small agent-side helper function to pre-filter list_tasks results before final prompt (only if Cohere struggles)
  - system_prompt_key_additions:
    """
    - NEVER ask for or mention numeric task IDs — users don't know them.
    - Always use task titles to identify which task the user means.
    - When the user says "complete X", "delete Y", "update Z" — internally:
      1. Call list_tasks to get current tasks
      2. Find best title match
      3. If unique → use its id for the action tool
      4. If multiple → ask user to choose by title or number (show titles only)
      5. If none → tell user and suggest alternatives
    - In all responses: refer to tasks by their titles, never by ID.
    """
  - organize_by_phases: Prompt Rewrite → Few-Shot Examples → Resolution Rules → Clarification Templates → Full Flow Testing

Result goal: User feels like they're talking to a real assistant who remembers task names — no IDs ever mentioned or requested.
```

## Response Text

Successfully created a comprehensive implementation plan for the Phase III Extension to enable natural task reference by title, eliminating the need for users to provide numeric Task IDs during operations.

## Outcome Impact

Created a complete implementation plan with research, data models, quickstart guide, and API contracts that addresses the requirements for improving chatbot UX by removing numeric Task ID dependencies and enabling natural language task management.

## Tests Summary

None

## Files Summary

- specs/5-natural-task-reference-by-title/plan.md
- specs/5-natural-task-reference-by-title/research.md
- specs/5-natural-task-reference-by-title/data-model.md
- specs/5-natural-task-reference-by-title/quickstart.md
- specs/5-natural-task-reference-by-title/contracts/title-resolution-api.yaml

## Next Prompts

Generate tasks for the implementation of the natural task reference by title feature, or implement the changes according to the plan.

## Reflection Note

The implementation plan effectively addresses the core challenge of enabling natural language task management while maintaining security and system integrity.

## Evaluation Notes

Failure modes observed: The automated plan creation script was not available, so manual creation was necessary.

Next experiment to improve prompt quality: Ensure proper setup scripts are available in the environment for streamlined planning workflow.