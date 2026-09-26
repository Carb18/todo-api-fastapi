from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_all_tasks, get_task_by_id, create_task



class TaskCreate(BaseModel):
    title: str
    description: str
   
class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None

app = FastAPI()
init_db()



#root Endpoint
@app.get("/")
async def read_root():
    return {"name": "Task API", 
            "version": "1.0", 
            "description": "API for managing tasks",
            "endpoints": ["/tasks"]}


# Endpoint to get the health status of the API    
@app.get("/health")
async def read_health():
    return {"status": "ok", "message": "API is healthy and running."}

# Endpoint to get all tasks
@app.get("/tasks")
def get_tasks():
    return get_all_tasks()

# Endpoint to get a specific task by ID

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

# Endpoint to create a new task
@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return create_task(task.title, task.description)


