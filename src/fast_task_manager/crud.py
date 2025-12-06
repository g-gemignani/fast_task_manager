from sqlalchemy.orm import Session
from . import models, schemas

# Function to get a single task
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Function to get a list of tasks
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# Function to create a new task
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Function to delete a task
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

# Function to update a task (e.g., mark as completed)
def update_task_completion(db: Session, task_id: int, completed: bool):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task
    return None
