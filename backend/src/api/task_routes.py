from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..services.task_service import TaskService
from ..middleware.auth import get_current_user_id


router = APIRouter(tags=["Tasks"])


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: int,
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Input validation
    if not task_create.title or len(task_create.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is required"
        )

    if len(task_create.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be less than 255 characters"
        )

    if task_create.description and len(task_create.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be less than 1000 characters"
        )

    # Sanitize inputs - strip leading/trailing whitespace
    task_create.title = task_create.title.strip()
    if task_create.description:
        task_create.description = task_create.description.strip()

    return TaskService.create_task(session=session, task_create=task_create, user_id=user_id)


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def read_tasks(
    user_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    return TaskService.get_tasks_by_user(session=session, user_id=user_id)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def read_task(
    user_id: int,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    task = TaskService.update_task(
        session=session, task_id=task_id, task_update=task_update, user_id=user_id
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: int,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    success = TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: int,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    task = TaskService.toggle_task_completion(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task