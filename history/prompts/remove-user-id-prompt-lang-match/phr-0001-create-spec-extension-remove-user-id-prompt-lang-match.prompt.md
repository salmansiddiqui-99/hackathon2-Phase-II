---
id: "PHR-0001"
title: "Create Spec Extension Remove User ID Prompt Lang Match"
stage: "spec"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "remove-user-id-prompt-lang-match"
branch: "4-remove-user-id-prompt-lang-match"
user: "haroon traders"
command: "manual"
labels: ["spec", "user-authentication", "multi-language", "chatbot"]
links:
  spec: "specs/4-remove-user-id-prompt-lang-match/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/4-remove-user-id-prompt-lang-match/spec.md"
  - "specs/4-remove-user-id-prompt-lang-match/checklists/requirements.md"
  - "history/prompts/remove-user-id-prompt-lang-match/phr-0001-create-spec-extension-remove-user-id-prompt-lang-match.prompt.md"
tests: []
---

# Prompt History Record: Create Spec Extension Remove User ID Prompt Lang Match

## Prompt Text

Phase III Extension: Remove explicit User ID prompting + Add automatic multi-language response matching user's input language

Target audience: Hackathon participants and judges evaluating natural, frictionless chatbot UX and intelligent language handling

Focus: Improve the conversational experience of the Phase III AI Todo Chatbot so that:

1. The chatbot NEVER asks the user for their User ID when performing CRUD operations (add, update, complete, delete, list tasks)
2. The chatbot automatically detects the language used in the user's message and responds in the same language (multi-language support without explicit selection)

Success criteria:
- **User ID handling**:
  - The chatbot infers the authenticated user automatically from the JWT token sent with every /api/{user_id}/chat request
  - In all tool calls (add_task, list_tasks, complete_task, delete_task, update_task), the user_id parameter is filled from the authenticated context — never from user input
  - If the user tries to mention or provide a user ID in natural language, the agent ignores it and uses the authenticated one
  - No message ever contains phrases like "What is your user ID?", "Please provide your ID", "Whose tasks?", etc.
- **Language matching**:
  - Chatbot detects the primary language of the user's input message
  - All responses (normal text + confirmations + error messages) are generated in the same detected language
  - Supported languages at minimum: English + Urdu (as per bonus feature) + any major language the chosen LLM (Cohere Command family) handles well
  - System prompt updated to enforce: "Always respond in the exact same language the user is currently using"
  - Language detection is implicit (done by the LLM itself) — no external library required
- All Basic Level todo operations remain fully functional via natural language
- No regression in existing behavior (context preservation, tool calling accuracy, confirmation style)

Constraints:
- Must stay within current architecture: ChatKit → FastAPI /chat → OpenAI Agents SDK agent → Cohere Compatibility API → MCP tools
- User authentication & JWT still required (no anonymous mode)
- Do NOT add new database fields or change MCP tool signatures
- Language support implemented purely via system prompt engineering and LLM capabilities — no translation API
- Keep using Cohere Trial / Compatibility API layer (no model or provider change)
- All changes must be spec-driven and generated via Claude Code / subagents

Not building:
- Explicit language selection menu or command
- Asking user to choose language
- Storing preferred language per user in database
- Adding new endpoints or changing /chat signature
- Implementing client-side language detection
- Supporting right-to-left layout adjustments in ChatKit (UI remains LTR unless bonus CSS added)

Bonus alignment:
- Directly contributes to "Multi-language Support – Support Urdu in chatbot" (+100 points)
- Improves overall UX → higher chance of strong demo video impression

This extension makes the chatbot significantly more natural, user-friendly, and production-like while staying fully compliant with the hackathon Phase III requirements and architecture.

## Response Text

Successfully created a comprehensive specification for the Phase III Extension to remove explicit User ID prompting and add automatic multi-language response matching. Created spec file with user stories, functional requirements, and success criteria, plus a quality checklist.

## Outcome Impact

Created a complete feature specification that addresses the requirements for improving chatbot UX by removing user ID prompts and enabling automatic language matching. The specification includes all necessary details for planning and implementation.

## Tests Summary

None

## Files Summary

- specs/4-remove-user-id-prompt-lang-match/spec.md
- specs/4-remove-user-id-prompt-lang-match/checklists/requirements.md
- history/prompts/remove-user-id-prompt-lang-match/phr-0001-create-spec-extension-remove-user-id-prompt-lang-match.prompt.md

## Next Prompts

Plan implementation of the feature based on the specification, generate tasks for the implementation, or implement the changes to remove user ID prompting and add language detection.

## Reflection Note

Creating a comprehensive specification with user stories, functional requirements, and success criteria helps ensure the implementation will meet the desired user experience goals while maintaining security and language support requirements.

## Evaluation Notes

Failure modes observed: The sp.phr skill failed to execute due to missing bash script. Workaround was to manually create the PHR file with proper structure.

Next experiment to improve prompt quality: Ensure PHR creation scripts are available in the environment or provide fallback manual creation process.