"""
MCP Tools Implementation for Task Operations

This module implements the five required MCP tools for task management:
-add_task
-list_tasks
-complete_task
-delete_task
-update_task

Each tool enforces user ownership and returns consistent response formats.
"""
from typing import Dict, Any, List
from pydantic import BaseModel
from sqlmodel import Session, select
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService


class AddTaskParams(BaseModel):
    user_id: int
    title: str
    description: str = ""


class ListTasksParams(BaseModel):
    user_id: int


class CompleteTaskParams(BaseModel):
    user_id: int
    task_id: int


class DeleteTaskParams(BaseModel):
    user_id: int
    task_id: int


class UpdateTaskParams(BaseModel):
    user_id: int
    task_id: int
    title: str = None
    description: str = None
    completed: bool = None


def add_task(params: AddTaskParams) -> Dict[str, Any]:
    """
    Add a new task for the specified user.

    Args:
        params: Parameters including user_id, title, and optional description

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # Prepare task creation data
            task_create = TaskCreate(
                title=params.title,
                description=params.description,
                completed=False  # Default to not completed
            )

            # Use the TaskService to create the task
            created_task = TaskService.create_task(
                session=session,
                task_create=task_create,
                user_id=params.user_id
            )

            return {
                "task_id": created_task.id,
                "status": "success",
                "title": created_task.title
            }
    except Exception as e:
        return {
            "task_id": None,
            "status": "error",
            "title": "",
            "error": str(e)
        }


def list_tasks(params: ListTasksParams) -> Dict[str, Any]:
    """
    List all tasks for the specified user.

    Args:
        params: Parameters including user_id

    Returns:
        Dictionary with status and array of tasks
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # Use the TaskService to get tasks for the user
            tasks = TaskService.get_tasks_by_user(
                session=session,
                user_id=params.user_id
            )

            # Convert tasks to the required format
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            return {
                "status": "success",
                "tasks": task_list
            }
    except Exception as e:
        return {
            "status": "error",
            "tasks": [],
            "error": str(e)
        }


def complete_task(params: CompleteTaskParams) -> Dict[str, Any]:
    """
    Mark a task as completed for the specified user.

    Args:
        params: Parameters including user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # First, verify the task belongs to the user by getting it
            task = TaskService.get_task_by_id(
                session=session,
                task_id=params.task_id,
                user_id=params.user_id
            )

            if not task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Task not found or access denied",
                    "error": "Task does not exist or does not belong to user"
                }

            # Prepare update data to mark as completed
            task_update = TaskUpdate(completed=True)

            # Use the TaskService to update the task
            updated_task = TaskService.update_task(
                session=session,
                task_id=params.task_id,
                task_update=task_update,
                user_id=params.user_id
            )

            if not updated_task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Failed to update task",
                    "error": "Could not complete task"
                }

            return {
                "task_id": updated_task.id,
                "status": "success",
                "title": updated_task.title
            }
    except Exception as e:
        return {
            "task_id": params.task_id,
            "status": "error",
            "title": "",
            "error": str(e)
        }


def delete_task(params: DeleteTaskParams) -> Dict[str, Any]:
    """
    Delete a task for the specified user.

    Args:
        params: Parameters including user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # Get the task first to retrieve its title for the response
            task = TaskService.get_task_by_id(
                session=session,
                task_id=params.task_id,
                user_id=params.user_id
            )

            if not task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Task not found or access denied",
                    "error": "Task does not exist or does not belong to user"
                }

            # Use the TaskService to delete the task
            success = TaskService.delete_task(
                session=session,
                task_id=params.task_id,
                user_id=params.user_id
            )

            if not success:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Failed to delete task",
                    "error": "Could not delete task"
                }

            return {
                "task_id": task.id,
                "status": "success",
                "title": task.title
            }
    except Exception as e:
        return {
            "task_id": params.task_id,
            "status": "error",
            "title": "",
            "error": str(e)
        }


def update_task(params: UpdateTaskParams) -> Dict[str, Any]:
    """
    Update a task for the specified user.

    Args:
        params: Parameters including user_id, task_id, and optional fields to update

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # First, verify the task belongs to the user by getting it
            existing_task = TaskService.get_task_by_id(
                session=session,
                task_id=params.task_id,
                user_id=params.user_id
            )

            if not existing_task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Task not found or access denied",
                    "error": "Task does not exist or does not belong to user"
                }

            # Prepare update data with only the fields that were provided
            update_data = {}
            if params.title is not None:
                update_data["title"] = params.title
            if params.description is not None:
                update_data["description"] = params.description
            if params.completed is not None:
                update_data["completed"] = params.completed

            # If no fields to update, return error
            if not update_data:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "No updates provided",
                    "error": "No fields to update"
                }

            task_update = TaskUpdate(**update_data)

            # Use the TaskService to update the task
            updated_task = TaskService.update_task(
                session=session,
                task_id=params.task_id,
                task_update=task_update,
                user_id=params.user_id
            )

            if not updated_task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Task not found or access denied",
                    "error": "Task does not exist or does not belong to user"
                }

            return {
                "task_id": updated_task.id,
                "status": "success",
                "title": updated_task.title
            }
    except Exception as e:
        return {
            "task_id": params.task_id,
            "status": "error",
            "title": "",
            "error": str(e)
        }


def toggle_task_completion(params: CompleteTaskParams) -> Dict[str, Any]:
    """
    Toggle the completion status of a task for the specified user.

    Args:
        params: Parameters including user_id and task_id

    Returns:
        Dictionary with task_id, status, title, and completion status
    """
    try:
        # Create a new database session
        with next(get_session()) as session:
            # Use the TaskService to toggle the task completion
            updated_task = TaskService.toggle_task_completion(
                session=session,
                task_id=params.task_id,
                user_id=params.user_id
            )

            if not updated_task:
                return {
                    "task_id": params.task_id,
                    "status": "error",
                    "title": "Task not found or access denied",
                    "error": "Task does not exist or does not belong to user"
                }

            return {
                "task_id": updated_task.id,
                "status": "success",
                "title": updated_task.title,
                "completed": updated_task.completed
            }
    except Exception as e:
        return {
            "task_id": params.task_id,
            "status": "error",
            "title": "",
            "completed": None,
            "error": str(e)
        }


# Export the functions
__all__ = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task", "toggle_task_completion"]