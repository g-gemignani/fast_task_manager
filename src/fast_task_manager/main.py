from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Endpoints ##

# 1. Create a Task
@app.post("/tasks/", response_model=schemas.Task)
def create_task_endpoint(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

# 2. Read All Tasks
@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

# 3. Read Single Task
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# 4. Update Task Completion
@app.put("/tasks/{task_id}/complete", response_model=schemas.Task)
def toggle_task_completion(task_id: int, completed: bool = True, db: Session = Depends(get_db)):
    updated_task = crud.update_task_completion(db, task_id=task_id, completed=completed)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# 5. Delete Task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
