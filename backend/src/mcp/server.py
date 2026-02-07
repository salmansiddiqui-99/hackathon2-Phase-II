"""
MCP Server for Task Management Tools

This module implements an MCP (Model Context Protocol) server that exposes
task management tools to AI agents.
"""
from typing import Dict, Any, Callable
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import json
from .tools import (
    add_task, list_tasks, complete_task, delete_task, update_task,
    AddTaskParams, ListTasksParams, CompleteTaskParams,
    DeleteTaskParams, UpdateTaskParams
)


class MCPServer:
    """
    MCP Server that manages and exposes tools to AI agents
    """

    def __init__(self):
        self.tools = {
            "add_task": {
                "function": add_task,
                "param_model": AddTaskParams
            },
            "list_tasks": {
                "function": list_tasks,
                "param_model": ListTasksParams
            },
            "complete_task": {
                "function": complete_task,
                "param_model": CompleteTaskParams
            },
            "delete_task": {
                "function": delete_task,
                "param_model": DeleteTaskParams
            },
            "update_task": {
                "function": update_task,
                "param_model": UpdateTaskParams
            }
        }

    def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific tool with the provided parameters

        Args:
            tool_name: Name of the tool to call
            params: Parameters to pass to the tool

        Returns:
            Result from the tool call
        """
        if tool_name not in self.tools:
            return {
                "status": "error",
                "error": f"Tool '{tool_name}' not found",
                "result": None
            }

        tool_info = self.tools[tool_name]
        param_model = tool_info["param_model"]

        try:
            # Validate parameters using Pydantic model
            validated_params = param_model(**params)

            # Call the tool function
            result = tool_info["function"](validated_params)

            return {
                "status": "success",
                "result": result,
                "error": None
            }
        except Exception as e:
            return {
                "status": "error",
                "result": None,
                "error": str(e)
            }

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """
        Get the schema for a specific tool

        Args:
            tool_name: Name of the tool

        Returns:
            Schema definition for the tool
        """
        if tool_name not in self.tools:
            return None

        # For simplicity, we'll return basic info about the tool
        # In a real MCP implementation, this would return the full JSON schema
        param_model = self.tools[tool_name]["param_model"]

        # Create a basic schema representation
        schema = {
            "name": tool_name,
            "description": f"Tool to handle {tool_name.replace('_', ' ')} operations",
            "parameters": param_model.model_json_schema()
        }

        return schema

    def get_all_tools_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get schemas for all available tools

        Returns:
            Dictionary containing schemas for all tools
        """
        schemas = {}
        for tool_name in self.tools.keys():
            schemas[tool_name] = self.get_tool_schema(tool_name)
        return schemas


# Global MCP server instance
mcp_server = MCPServer()


def get_mcp_server():
    """
    Get the global MCP server instance
    """
    return mcp_server


# If running as a standalone server, you might have a main entry point
if __name__ == "__main__":
    # Example of how to use the server
    server = MCPServer()

    # Example tool call
    result = server.call_tool("list_tasks", {"user_id": 1})
    print(json.dumps(result, indent=2))