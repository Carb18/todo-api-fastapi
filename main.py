from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import (init_db,
                      get_all_tasks,
                      get_task_by_id,
                      create_task,
                      update_task,
                      delete_task)



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
@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return get_all_tasks()

# Endpoint to get a specific task by ID

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

# Endpoint to create a new task
@app.post("/tasks", status_code=201, response_model=Task)
def add_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return create_task(task.title, task.description)

# Endpoint to update a specific task
@app.put("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, task: TaskUpdate):
    updated = update_task(task_id, task.title, task.description, task.done)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task with ID {task_id} not found")
    return updated

# Endpoint to delete a specific task
@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task with ID {task_id} not found")


