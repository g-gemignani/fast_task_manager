from pydantic import BaseModel

# Schema for creating/updating a Task (doesn't need 'id' or 'completed' status initially)
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

# Schema for reading a Task (the response model)
class Task(TaskCreate):
    id: int
    completed: bool

    class Config:
        # Allows Pydantic to read data from SQLAlchemy model (ORM mode)
        from_attributes = True
