from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    # The assignment wants {"error": "..."} instead of FastAPI's default {"detail": "..."}
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# --- In-memory "database" ---------------------------------------------
# A plain list of dicts. Resets every time the server restarts —
# that's expected at this stage; a real database comes in Week 3.
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Walk the dog", "done": True},
]
next_id = 4


def find_task(task_id: int):
    """Return the task with this id, or None if it doesn't exist."""
    return next((t for t in tasks if t["id"] == task_id), None)


@app.get("/", summary="API info")
def root():
    """Describes what this API is and where to find its main resource."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check")
def health():
    """Used to confirm the server is up and responding."""
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def list_tasks():
    """Returns every task currently in memory."""
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(body: TaskCreate):
    """Creates a task from a JSON body like {"title": "Buy milk"}. Title is required."""
    global next_id
    if not body.title or not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, body: TaskUpdate):
    """Updates a task's title and/or done status. At least one field is required."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if body.title is None and body.done is None:
        raise HTTPException(status_code=400, detail="provide title and/or done to update")
    if body.title is not None and not body.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")

    if body.title is not None:
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task permanently. Returns no body on success."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return None
