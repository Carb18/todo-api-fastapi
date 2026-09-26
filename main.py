from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_all_tasks, get_task_by_id



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
@app.post("/tasks", description="Create a new task", status_code=201)
async def create_task(task: TaskCreate):
   if task.title == "" or task.description == "":
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")
   new_task = Task(id=len(tasks) + 1, title=task.title, description=task.description, done=False)
   tasks.append(new_task)
   return new_task

@app.put("/tasks/{task_id}", description="Update a task")
async def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if updated_task.title == "" or updated_task.description == "":
                raise HTTPException(status_code=400, detail="Title and description cannot be empty")
            if updated_task.title is not None:
                task.title = updated_task.title
            if updated_task.description is not None:
                task.description = updated_task.description
            if updated_task.done is not None:
                task.done = updated_task.done
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

@app.delete("/tasks/{task_id}", description="Delete a task", status_code=204)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")