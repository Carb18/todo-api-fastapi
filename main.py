from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
   
class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool


app = FastAPI()

tasks = [Task(id=1, title="Task 1", description="Shut down the server", done=False),
         Task(id=2, title="Task 2", description="Buy some pancakes", done=True),
         Task(id=3, title="Task 3", description="Write a blog post", done=False)]


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
async def get_tasks():
    return tasks

# Endpoint to get a specific task by ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

# Endpoint to create a new task
@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
   if task.title == "" or task.description == "":
        raise HTTPException(status_code=400, detail="Title and description cannot be empty")
   new_task = Task(id=len(tasks) + 1, title=task.title, description=task.description, done=False)
   tasks.append(new_task)
   return new_task