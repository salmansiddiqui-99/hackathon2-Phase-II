"""
Task Resolver Module

This module provides functionality to resolve task titles to task IDs using
exact matches, partial matches, and fuzzy matching algorithms.
"""

from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from difflib import SequenceMatcher
from ..database import get_session
from ..models.task import Task
from ..services.task_service import TaskService


class TaskResolver:
    """Resolves task titles to task IDs with various matching strategies"""

    @staticmethod
    def get_all_tasks_for_user(session: Session, user_id: int) -> List[Task]:
        """
        Get all tasks for a specific user

        Args:
            session: Database session
            user_id: User ID to retrieve tasks for

        Returns:
            List of Task objects for the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def exact_match(tasks: List[Task], title: str) -> Optional[Task]:
        """
        Find exact match for a task title (case-insensitive)

        Args:
            tasks: List of tasks to search
            title: Title to match exactly

        Returns:
            Matching task if found, None otherwise
        """
        title_lower = title.lower().strip()
        for task in tasks:
            if task.title.lower().strip() == title_lower:
                return task
        return None

    @staticmethod
    def partial_match(tasks: List[Task], title: str) -> Optional[Task]:
        """
        Find partial match where the input title contains the task title or vice versa

        Args:
            tasks: List of tasks to search
            title: Title to match partially

        Returns:
            Matching task if found, None otherwise
        """
        title_lower = title.lower().strip()
        for task in tasks:
            task_title_lower = task.title.lower().strip()
            if title_lower in task_title_lower or task_title_lower in title_lower:
                return task
        return None

    @staticmethod
    def fuzzy_match(tasks: List[Task], title: str, threshold: float = 0.6) -> Optional[Task]:
        """
        Find fuzzy match using sequence matching algorithm

        Args:
            tasks: List of tasks to search
            title: Title to match fuzzily
            threshold: Minimum similarity ratio (0.0 to 1.0)

        Returns:
            Best matching task if similarity exceeds threshold, None otherwise
        """
        title_lower = title.lower().strip()
        best_match = None
        best_ratio = 0.0

        for task in tasks:
            task_title_lower = task.title.lower().strip()
            # Calculate similarity ratio
            ratio = SequenceMatcher(None, title_lower, task_title_lower).ratio()

            if ratio >= threshold and ratio > best_ratio:
                best_ratio = ratio
                best_match = task

        return best_match

    @staticmethod
    def resolve_task_id_by_title(user_id: int, title_query: str) -> Dict[str, Any]:
        """
        Main method to resolve a title query to a task ID using multiple matching strategies

        Args:
            user_id: User ID to search tasks for
            title_query: Title to search for

        Returns:
            Dictionary containing result information
        """
        with next(get_session()) as session:
            # Get all tasks for the user
            tasks = TaskResolver.get_all_tasks_for_user(session, user_id)

            if not tasks:
                return {
                    "status": "error",
                    "message": "No tasks found for this user",
                    "task_id": None,
                    "matched_title": None,
                    "match_type": None
                }

            # Try exact match first
            matched_task = TaskResolver.exact_match(tasks, title_query)
            if matched_task:
                return {
                    "status": "success",
                    "message": "Exact match found",
                    "task_id": matched_task.id,
                    "matched_title": matched_task.title,
                    "match_type": "exact"
                }

            # Try partial match
            matched_task = TaskResolver.partial_match(tasks, title_query)
            if matched_task:
                return {
                    "status": "success",
                    "message": "Partial match found",
                    "task_id": matched_task.id,
                    "matched_title": matched_task.title,
                    "match_type": "partial"
                }

            # Try fuzzy match
            matched_task = TaskResolver.fuzzy_match(tasks, title_query)
            if matched_task:
                return {
                    "status": "success",
                    "message": "Fuzzy match found",
                    "task_id": matched_task.id,
                    "matched_title": matched_task.title,
                    "match_type": "fuzzy"
                }

            # No match found
            # Return list of available tasks for clarification
            task_titles = [task.title for task in tasks]
            return {
                "status": "not_found",
                "message": f"No task found matching '{title_query}'. Available tasks: {', '.join(task_titles[:5])}",
                "task_id": None,
                "matched_title": None,
                "match_type": None,
                "available_tasks": task_titles
            }

    @staticmethod
    def resolve_multiple_tasks_by_title(user_id: int, title_queries: List[str]) -> List[Dict[str, Any]]:
        """
        Resolve multiple title queries to task IDs

        Args:
            user_id: User ID to search tasks for
            title_queries: List of titles to search for

        Returns:
            List of dictionaries with resolution results
        """
        results = []
        for title_query in title_queries:
            result = TaskResolver.resolve_task_id_by_title(user_id, title_query)
            results.append(result)
        return results