---
id: "PHR-0001"
title: "Create Spec Natural Task Ref By Title"
stage: "spec"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "natural-task-reference-by-title"
branch: "5-natural-task-reference-by-title"
user: "haroon traders"
command: "manual"
labels: ["spec", "task-management", "natural-language", "chatbot"]
links:
  spec: "specs/5-natural-task-reference-by-title/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/5-natural-task-reference-by-title/spec.md"
  - "specs/5-natural-task-reference-by-title/checklists/requirements.md"
  - "history/prompts/natural-task-reference-by-title/phr-0001-create-spec-natural-task-ref-by-title.prompt.md"
tests: []
---

# Prompt History Record: Create Spec Natural Task Ref By Title

## Prompt Text

Phase III Extension: Natural Task Reference by Title (No Task ID Prompting)

Target audience: Hackathon participants and judges evaluating natural, frictionless, human-like chatbot conversation design

Focus: Make the Phase III AI Todo Chatbot handle update, complete, delete, and (if ambiguous) list operations using **task title** instead of requiring the user to know or provide numeric Task IDs.

The goal is to eliminate all prompts asking for Task ID — similar to how we already removed User ID prompting.

Success criteria:
- The chatbot **never** asks the user for a numeric Task ID in any scenario
- Supported natural language patterns that should work without ID:
  - "complete my task buy groceries"
  - "mark 'call mom' as done"
  - "delete the task named finish report"
  - "update 'morning run' to 'morning yoga at 7am'"
  - "reschedule my dentist appointment to next Tuesday"
- When title is ambiguous (multiple tasks with very similar/identical titles):
  - Chatbot asks for **clarification by showing short list of matching titles** (not IDs)
  - Example response:
    "I found two tasks with similar titles:
    1. buy groceries
    2. buy groceries for party
    Which one do you mean?"
  - User can reply with number (1/2), full title, or more detail → chatbot proceeds
- When title is unique → action is performed silently and confirmed
- List operation ("show my tasks", "list todos") still shows tasks with titles + status + other visible fields — no IDs shown to user unless absolutely necessary for disambiguation
- Add / update still work by title (creation doesn't need ID anyway)
- All previous improvements remain:
  - No User ID ever asked
  - Responses in the same language the user is using
- Maintains 100% correctness: wrong title → helpful message ("I couldn't find a task called 'xyz'. Here are your current tasks: …")

Constraints:
- Do **not** change the MCP tool signatures (they still expect task_id internally)
- The intelligence to map title → task_id must happen **inside the agent / before tool call**
  - Agent queries list_tasks first (internally) when title-based command is detected
  - Matches title (case-insensitive, partial match with tolerance)
  - If exactly one match → use its id for complete/delete/update
  - If multiple → ask user for clarification (text response, no tool call yet)
  - If none → inform user and optionally list recent/open tasks
- Implementation must stay within current stack:
  - OpenAI Agents SDK + Cohere Compatibility API
  - Existing 5 MCP tools
  - Stateless /chat endpoint
  - No new database queries outside existing tools
- All logic implemented via **stronger system prompt + possible few-shot examples**
  - Preferred: pure prompt engineering (zero code change to tools or endpoint)
  - Allowed: small wrapper/helper function inside agent if prompt alone is not reliable enough
- Keep demo-friendly: short, clear clarification messages

Not building:
- Showing internal Task IDs to the user in normal flow
- Forcing user to use numbers/IDs
- Adding new MCP tools (e.g. get_task_by_title)
- Changing database schema
- Client-side title search (everything server/agent side)
- Strict exact-match-only (fuzzy/partial matching should be supported via LLM reasoning)

Bonus alignment:
- Makes chatbot significantly more user-friendly and natural
- Directly improves UX score in judging (especially in demo video)
- Builds on previous "no user ID" and "multi-language" improvements

This change removes the last major point of friction in title-based task management — users should be able to speak to the bot like they would speak to a human assistant.

## Response Text

Successfully created a comprehensive specification for the Phase III Extension to enable natural task reference by title, eliminating the need for users to provide numeric Task IDs during operations.

## Outcome Impact

Created a complete feature specification that addresses the requirements for improving chatbot UX by removing numeric Task ID dependencies and enabling natural language task management.

## Tests Summary

None

## Files Summary

- specs/5-natural-task-reference-by-title/spec.md
- specs/5-natural-task-reference-by-title/checklists/requirements.md
- history/prompts/natural-task-reference-by-title/phr-0001-create-spec-natural-task-ref-by-title.prompt.md

## Next Prompts

Plan implementation of the feature based on the specification, generate tasks for the implementation, or implement the changes to enable natural task reference by title.

## Reflection Note

Creating a comprehensive specification with user stories, functional requirements, and success criteria helps ensure the implementation will meet the desired user experience goals while maintaining compatibility with existing functionality.

## Evaluation Notes

Failure modes observed: The automated script wasn't available, so manual creation was necessary.

Next experiment to improve prompt quality: Ensure proper automation scripts are available in the environment for streamlined specification creation.