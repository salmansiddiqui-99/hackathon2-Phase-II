"""
AI Agent Module

This module creates and manages the AI agent that processes natural language
requests and orchestrates MCP tools for task operations using Cohere API.
"""

import os
from typing import Dict, Any, List
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .cohere_config import cohere_client, get_default_model
from ..mcp.server import get_mcp_server
from ..mcp.tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskParams, ListTasksParams, CompleteTaskParams,
    DeleteTaskParams, UpdateTaskParams
)
from ..logging_config import logger
from ..utils.language_detection import language_detector, localization_manager
from .task_resolver import TaskResolver

# Load environment variables
load_dotenv()


class AIAgent:
    """
    AI Agent that processes natural language requests and orchestrates MCP tools
    """

    def __init__(self):
        self.client = cohere_client  # Updated to use Cohere client
        self.model = get_default_model()  # Updated to use Cohere model
        self.mcp_server = get_mcp_server()

        # Define the tools that the AI agent can use
        # We'll keep the user_id in the tools definition for clarity but inject it automatically
        # Enhanced tools now support both task IDs and titles for operations
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed. The task can be specified by ID or by title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {
                                "anyOf": [
                                    {"type": "integer", "description": "The ID of the task to complete"},
                                    {"type": "string", "description": "The title of the task to complete"}
                                ]
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task. You MUST explicitly confirm with the user before deleting the task. The task can be specified by ID or by title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {
                                "anyOf": [
                                    {"type": "integer", "description": "The ID of the task to delete"},
                                    {"type": "string", "description": "The title of the task to delete"}
                                ]
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task. The task can be specified by ID or by title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "The ID of the user"},
                            "task_id": {
                                "anyOf": [
                                    {"type": "integer", "description": "The ID of the task to update"},
                                    {"type": "string", "description": "The title of the task to update"}
                                ]
                            },
                            "title": {"type": "string", "description": "The new title for the task (optional)"},
                            "description": {"type": "string", "description": "The new description for the task (optional)"},
                            "completed": {"type": "boolean", "description": "The new completion status (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    def process_request(self, user_id: int, message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a natural language request and return an appropriate response.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language request from the user
            conversation_history: Optional history of previous messages in the conversation

        Returns:
            Dictionary with response and any tool calls made
        """
        # Detect language from user message
        detected_lang, confidence = language_detector.detect_language(message)

        logger.info(f"Processing request for user {user_id} in language {detected_lang} (confidence: {confidence:.2f}): {message}")

        try:
            # Prepare the messages for the AI model
            messages = []

            # Add system message with enhanced instructions for task confirmation and error handling
            system_message = f"""You are an AI assistant that helps users manage their tasks. Use the available tools to perform task operations. Always respect the user's identity and only operate on tasks belonging to the current user.

CRITICAL RULES:
1. For DELETE operations: You MUST explicitly ask for user confirmation before deleting any task. Only proceed with deletion if the user confirms. You can detect user confirmation in phrases like 'yes', 'confirm', 'proceed', 'delete it', etc.
2. For UPDATE operations: Always confirm significant changes with the user before updating, especially for titles and descriptions.
3. If a tool operation fails, report the error back to the user.
4. Only perform operations that the user has explicitly requested.
5. The user_id is automatically handled by the system - do not include it in your tool calls.
6. NEVER ask users for task IDs. Users can refer to tasks by their titles or partial titles.
7. When users mention tasks by title, the system will automatically resolve them to the correct task IDs.
8. Always refer to tasks by their titles in your responses, not by their IDs.
9. For title-based operations, the system supports exact matches, partial matches, and fuzzy matching.
10. When clarification is needed, show the user a list of their available tasks to help them identify the correct one.

FEW-SHOT EXAMPLES FOR TITLE-BASED TASK RESOLUTION:
- User: "Complete my grocery shopping task"
- Assistant: Uses exact or partial matching to find a task titled "Grocery Shopping" and completes it
- User: "Update meeting notes task with new content"
- Assistant: Finds the task titled "Meeting Notes" or similar and updates it
- User: "Delete task about cleaning"
- Assistant: Looks for tasks with "cleaning" in the title and offers to delete the best match
- User: "Mark 'prepare presentation' as done"
- Assistant: Matches "prepare presentation" against task titles and marks the corresponding task as completed"""

            # Add language-specific instructions if confidence is high enough
            if confidence > 0.5 and detected_lang != 'en':
                system_message += f"\n11. Respond in the user's language ({language_detector.get_language_name(detected_lang)})."

            # Add language-specific instructions if confidence is high enough
            if confidence > 0.5 and detected_lang != 'en':
                system_message += f"\n6. Respond in the user's language ({language_detector.get_language_name(detected_lang)})."

            messages.append({
                "role": "system",
                "content": system_message
            })

            # Add conversation history if available
            if conversation_history:
                logger.debug(f"Including {len(conversation_history)} messages from conversation history for user {user_id}")
                for msg in conversation_history:
                    messages.append(msg)

            # Add the current user message
            messages.append({
                "role": "user",
                "content": message
            })

            # Call the Cohere API with function calling (using OpenAI-compatible format)
            logger.debug(f"Calling Cohere API for user {user_id}")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
            except Exception as e:
                # Handle Cohere API failures
                logger.error(f"Cohere API error for user {user_id}: {str(e)}")
                return {
                    "response": f"Sorry, I'm currently unable to process your request due to a connection issue. Please try again later.",
                    "tool_calls": [],
                    "tool_results": [],
                    "error": f"Cohere API error: {str(e)}"
                }

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                logger.info(f"Processing {len(tool_calls)} tool calls for user {user_id}")

                # Process any tool calls
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Automatically inject the user_id into function arguments
                    function_args['user_id'] = user_id

                    logger.info(f"Calling tool {function_name} for user {user_id} with args: {function_args}")

                    # Call the appropriate MCP tool
                    result = self._call_mcp_tool(function_name, function_args)
                    logger.info(f"Tool {function_name} result: {result}")

                    # Add tool result - simplified format for Cohere compatibility
                    tool_results.append({
                        "role": "tool",
                        "content": json.dumps(result)
                    })

                # For Cohere compatibility, return the result of the tool call directly
                # Rather than making a second API call which causes the tool_call_id mismatch
                logger.info(f"Successfully processed request for user {user_id}, returning tool result")

                # Format a user-friendly response based on the tool result and language
                response_text = ""

                # Process each tool result to create appropriate response
                for tool_result in tool_results:
                    result = json.loads(tool_result["content"])

                    if result.get("status") == "success":
                        if "title" in result and "task_id" in result:
                            # For add_task
                            response_text = localization_manager.get_response(
                                detected_lang,
                                'task_added',
                                title=result['title'],
                                task_id=result['task_id']
                            )
                        elif "tasks" in result:
                            # For list_tasks - format the task list nicely
                            tasks = result["tasks"]
                            if tasks:
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'tasks_list_header',
                                    count=len(tasks)
                                ) + "\n"
                                for task in tasks:
                                    status = "COMPLETED" if task.get("completed", False) else "PENDING"
                                    response_text += f"  [{status}] {task['title']}"
                                    if task.get('description'):
                                        response_text += f" - {task['description']}"
                                    response_text += "\n"
                            else:
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'tasks_list_empty'
                                )
                        elif "task_id" in result and "completed" in result:
                            # For complete_task - specific handling
                            if result.get("completed", False):
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'task_completed',
                                    title=result.get('title', 'task')
                                )
                            else:
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'task_incomplete',
                                    title=result.get('title', 'task')
                                )
                        elif "task_id" in result:
                            # For other task operations like update_task
                            # Always try to use the title if available
                            title = result.get('title', f'task with ID {result["task_id"]}')
                            response_text = localization_manager.get_response(
                                detected_lang,
                                'task_updated',
                                title=title
                            )
                        elif "message" in result:
                            # Generic message
                            response_text = result["message"]
                        else:
                            # Generic success
                            response_text = localization_manager.get_response(
                                detected_lang,
                                'operation_success'
                            )
                    else:
                        # Handle error case
                        if result.get("status") == "not_found":
                            # Special handling for title resolution failures
                            available_tasks = result.get("available_tasks", [])
                            if available_tasks:
                                task_list_str = ", ".join(available_tasks[:5])  # Show first 5 tasks
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'task_not_found_with_suggestions',
                                    title_query=result.get("message", ""),
                                    available_tasks=task_list_str
                                )
                            else:
                                response_text = localization_manager.get_response(
                                    detected_lang,
                                    'task_not_found',
                                    title_query=result.get("message", "")
                                )
                        else:
                            error_msg = result.get("error", "Unknown error occurred")
                            response_text = localization_manager.get_response(
                                detected_lang,
                                'error_occurred',
                                error=error_msg
                            )

                return {
                    "response": response_text,
                    "tool_calls": [{"id": tc.id, "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in tool_calls],
                    "tool_results": tool_results
                }
            else:
                # No tool calls were made, return the AI's response directly
                logger.info(f"No tool calls needed for user {user_id}, returning direct response")

                # If the AI response seems to be in a different language than detected,
                # we might want to align it, but typically the AI follows the language of the conversation
                return {
                    "response": response_message.content,
                    "tool_calls": [],
                    "tool_results": []
                }

        except Exception as e:
            logger.error(f"Error processing request for user {user_id}: {str(e)}")
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": [],
                "tool_results": []
            }

    def _call_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the appropriate MCP tool with the given parameters.

        Args:
            tool_name: Name of the tool to call
            params: Parameters to pass to the tool

        Returns:
            Result from the tool call
        """
        try:
            if tool_name == "add_task":
                args = AddTaskParams(**params)
                return add_task(args)
            elif tool_name == "list_tasks":
                args = ListTasksParams(**params)
                return list_tasks(args)
            elif tool_name in ["complete_task", "delete_task", "update_task"]:
                # Handle task operations that may use titles instead of IDs
                # Check if task_id is provided as a string (likely a title) or looks like a title
                original_task_id = params.get("task_id")

                if (isinstance(original_task_id, str) and len(str(original_task_id)) > 0) or \
                   (isinstance(original_task_id, str) and str(original_task_id).isdigit() == False):
                    # This is likely a title, try to resolve it to a task ID
                    resolution_result = TaskResolver.resolve_task_id_by_title(
                        user_id=params["user_id"],
                        title_query=str(original_task_id)
                    )

                    if resolution_result["status"] == "success":
                        # Replace the title with the resolved task ID
                        params["task_id"] = resolution_result["task_id"]
                        logger.info(f"Resolved title '{original_task_id}' to task ID {resolution_result['task_id']} for user {params['user_id']}")
                    elif resolution_result["status"] == "not_found":
                        # If not found, return the resolution error
                        return resolution_result
                    else:
                        # Return other resolution errors
                        return resolution_result

                # Now call the appropriate tool with the resolved task ID
                if tool_name == "complete_task":
                    args = CompleteTaskParams(**params)
                    return complete_task(args)
                elif tool_name == "delete_task":
                    args = DeleteTaskParams(**params)
                    return delete_task(args)
                elif tool_name == "update_task":
                    args = UpdateTaskParams(**params)
                    return update_task(args)
            else:
                return {"status": "error", "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"status": "error", "error": f"Tool call failed: {str(e)}"}


# Global agent instance
ai_agent = AIAgent()


def get_ai_agent():
    """
    Get the global AI agent instance
    """
    return ai_agent