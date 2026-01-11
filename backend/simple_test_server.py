from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Todo API - Simple Test", version="1.0.0")

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory storage for testing
tasks_db: List[Task] = [
    Task(id=1, user_id=1, title="Sample task", description="This is a sample task", completed=False),
    Task(id=2, user_id=1, title="Another task", description="This is another task", completed=True)
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API - Simple Test Version"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api-test"}

@app.get("/api/{user_id}/tasks", response_model=List[Task])
def get_tasks(user_id: int):
    user_tasks = [task for task in tasks_db if task.user_id == user_id]
    return user_tasks

@app.post("/api/{user_id}/tasks", response_model=Task)
def create_task(user_id: int, task: Task):
    task.user_id = user_id
    task.id = max([t.id for t in tasks_db]) + 1 if tasks_db else 1
    tasks_db.append(task)
    return task

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)