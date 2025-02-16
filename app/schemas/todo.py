from pydantic import BaseModel
from typing import Optional
class TodoUpdate(BaseModel):
    title: Optional[str] = None  # Allow updating title, but it's optional
    description:Optional[str]= None
    completed: Optional[bool] = None  # Allow updating completion status

    class Config:
        orm_mode = True  # To read data from ORM models

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: str

    class Config:
        orm_mode = True

        