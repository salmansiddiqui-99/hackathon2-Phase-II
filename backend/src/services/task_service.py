from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from fastapi import HTTPException, status


class TaskService:
    """Service class to handle task-related operations"""

    @staticmethod
    def create_task(*, session: Session, task_create: TaskCreate, user_id: int) -> TaskRead:
        """
        Create a new task for a specific user
        """
        # Create task with all required fields
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id  # Assign the user_id to the task
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return TaskRead.model_validate(db_task)

    @staticmethod
    def get_task_by_id(*, session: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
        """
        Get a specific task by its ID for a specific user
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()
        if task is None:
            return None
        return TaskRead.model_validate(task)

    @staticmethod
    def get_tasks_by_user(*, session: Session, user_id: int) -> List[TaskRead]:
        """
        Get all tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return [TaskRead.model_validate(task) for task in tasks]

    @staticmethod
    def update_task(*, session: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[TaskRead]:
        """
        Update a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if db_task is None:
            return None

        # Update the task with the provided values
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        from datetime import datetime
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskRead.model_validate(db_task)

    @staticmethod
    def delete_task(*, session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if db_task is None:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(*, session: Session, task_id: int, user_id: int) -> Optional[TaskRead]:
        """
        Toggle the completion status of a specific task for a specific user
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if db_task is None:
            return None

        # Toggle the completion status
        db_task.completed = not db_task.completed
        from datetime import datetime
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskRead.model_validate(db_task)