---
id: 301
title: natural-task-reference-by-title.feature
stage: green
date_iso: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 3-ai-agent-chatkit
branch: 001-switch-llm-provider
user: haroon traders
command: feature-impl
labels:
  - task-management
  - natural-language
  - ai-agent
  - title-resolution
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
files_yaml:
  - C:\Users\haroon traders\Desktop\BACKUP\phase-III\backend\src\ai\agent.py
  - C:\Users\haroon traders\Desktop\BACKUP\phase-III\backend\src\ai\task_resolver.py
  - C:\Users\haroon traders\Desktop\BACKUP\phase-III\backend\src\utils\language_detection.py
tests_yaml:
  - test_title_resolution.py
prompt_text: |
  Implement the Phase III Extension: Natural Task Reference by Title feature. Specifically:

  Phase 1: Setup
  - Update system prompt to forbid asking for task IDs in backend/src/ai/agent.py
  - Add title-based reasoning guidelines to system prompt in backend/src/ai/agent.py
  - Add few-shot examples for title → task_id resolution in backend/src/ai/agent.py

  Phase 2: Foundational
  - Implement internal task resolution logic in backend/src/ai/agent.py
  - Create clarification response templates in backend/src/ai/agent.py
  - Update confirmation messages to use titles in backend/src/ai/agent.py
  - Implement fuzzy/partial title matching logic in backend/src/ai/agent.py
  - Ensure all responses refer to tasks by titles, not IDs in backend/src/ai/agent.py

  This implementation should allow users to interact with the AI chatbot using natural language that refers to tasks by their titles instead of requiring numeric Task IDs.
response_text: |
  Successfully implemented the Phase III Extension: Natural Task Reference by Title feature with both phases completed:

  Phase 1: Setup
  - Updated system prompt in backend/src/ai/agent.py to forbid asking for task IDs
  - Added title-based reasoning guidelines to system prompt
  - Added comprehensive few-shot examples for title → task_id resolution
  - Enhanced tool definitions to support both integer IDs and string titles

  Phase 2: Foundational
  - Created backend/src/ai/task_resolver.py with complete title resolution logic
  - Implemented exact, partial, and fuzzy matching algorithms
  - Updated agent.py with internal task resolution functionality
  - Created clarification response templates in localization manager
  - Updated confirmation messages to use titles consistently
  - Ensured all responses refer to tasks by titles, not IDs
  - Added proper error handling and user feedback for resolution failures

  Key features implemented:
  - Natural language task reference using titles
  - Automatic title-to-ID resolution
  - Fuzzy matching for typos and variations
  - Comprehensive error handling with suggestions
  - Multilingual support for all new responses
  - Backwards compatibility with existing ID-based operations

  The implementation allows users to interact naturally with the AI chatbot using phrases like "Complete my grocery shopping task" instead of requiring numeric task IDs.
outcome: |
  The Natural Task Reference by Title feature has been successfully implemented. Users can now refer to tasks by their titles instead of numeric IDs, improving the natural language interaction experience. The system supports exact, partial, and fuzzy matching to handle various ways users might refer to their tasks.
evaluation: |
  Feature validated through:
  - Code compilation and import tests
  - Unit testing of title resolution logic
  - Verification of localization template updates
  - Confirmation of system integration
  - Backwards compatibility maintained
---

# Natural Task Reference by Title Feature Implementation

## Overview
This feature enables users to interact with the AI chatbot using natural language that refers to tasks by their titles instead of requiring numeric Task IDs.

## Changes Made

### 1. System Prompt Updates (agent.py)
- Added rule forbidding requests for task IDs
- Added title-based reasoning guidelines
- Included comprehensive few-shot examples for title resolution

### 2. Task Resolution Logic (task_resolver.py)
- Created new module for title-to-ID resolution
- Implemented exact matching algorithm
- Implemented partial matching algorithm
- Implemented fuzzy matching using SequenceMatcher
- Added multi-strategy resolution approach

### 3. Agent Integration (agent.py)
- Updated _call_mcp_tool method to handle title-based operations
- Modified response formatting to use titles consistently
- Enhanced tool definitions to accept both IDs and titles
- Added proper error handling for resolution failures

### 4. Localization Support (language_detection.py)
- Added new response templates for resolution errors
- Included multilingual support for all new responses
- Maintained backwards compatibility with existing templates

## Usage Examples
Users can now say:
- "Complete my grocery shopping task" instead of "Complete task #1"
- "Delete the cleaning task" instead of "Delete task #2"
- "Update the presentation task" instead of "Update task #3"

The system will automatically resolve titles to correct task IDs using multiple matching strategies.