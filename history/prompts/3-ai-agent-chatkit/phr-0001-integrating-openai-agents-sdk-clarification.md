---
ID: phr-0001
TITLE: Integrating OpenAI Agents SDK Clarification
STAGE: red
DATE_ISO: 2026-02-04
SURFACE: agent
MODEL: claude-sonnet-4-5-20250929
FEATURE: 3-ai-agent-chatkit
BRANCH: 1-todo-fullstack-web
USER: User
COMMAND: Clarify integration of OpenAI Agents SDK
LABELS: ["ai-agent", "chatkit", "sdk-integration", "tool-use", "conversation-history", "clarification"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - C:/Users/haroon traders/Desktop/phase-III/backend/src/ai/agent.py
TESTS_YAML:
  - null
PROMPT_TEXT: |
  The chatbot is not working. Please fix the issue and implement the provided OpenAI Agents SDK code in `agent.py`. The code should configure the OpenRouter client with `gemini-2.0-flash` model and use the provided `external_Client`. Ensure the agent is initialized with the specified instructions and the `Runner.run_sync` method is used with the `config` and `agent` objects.

  Here is the example code to integrate:
  ```python
  from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

  import os
  from dotenv import load_dotenv

  load_dotenv()

  gemini_api_key = os.getenv("GEMINI_API_KEY")

  external_Client = AsyncOpenAI(
      api_key=gemini_api_key,
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

  model = OpenAIChatCompletionsModel(
      model = "gemini-2.0-flash",
      openai_client = external_Client

  )

  config = RunConfig(
      model=model,
      model_provider = external_Client,
      tracing_disabled=True
  )

  agent = Agent(
      name = "Professional Front-End Designer",
      instructions= "Hello, How are you, Act as an Frontend Expert",
  )

  result = Runner.run_sync(
  agent,
  input="How are you",
  run_config=config
  )

  print (result.final_output)
  ```
RESPONSE_TEXT: |
  I have reviewed the `agent.py` file and the provided OpenAI Agents SDK code. Integrating the new SDK requires a significant change to how the AI agent processes requests, especially regarding tool calls and conversation history. The provided SDK example focuses on a single input and does not detail how to define and use tools or manage multi-turn conversations within its framework.

  To ensure I implement this correctly and preserve existing functionality as per the project guidelines, I need some clarification.

  1.  How should the existing MCP tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) be integrated into the new `agents` SDK framework? The provided example does not show how to define tools for the `Agent` object.
  2.  The original `process_request` method handled `conversation_history`. How should conversation history be managed when using `Runner.run_sync` from the `agents` SDK, which appears to take a single `input`?
  3.  The example `agent` is initialized with "Hello, How are you, Act as an Frontend Expert". Is this instruction meant to replace the existing system message for task management, or should the new agent also be capable of task management, and if so, how should the instructions be combined?
OUTCOME: Clarification requested for OpenAI Agents SDK integration, tool usage, and conversation history management.
EVALUATION: The PHR captures the user's prompt, the context of the issue (chatbot not working, integration of new SDK), the current state of `agent.py`, and the specific questions asked for clarification regarding tool integration and conversation history.
