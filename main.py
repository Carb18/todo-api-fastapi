from fastapi import FastAPI, HTTPException


app = FastAPI()

tasks = [{"id": 1, "title": "Task 1", "description": "Shut down the server", "completed": False},
         {"id": 2, "title": "Task 2", "description": "Buy some pancakes", "completed": True},
         {"id": 3, "title": "Task 3", "description": "Write a blog post", "completed": False}]


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

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")