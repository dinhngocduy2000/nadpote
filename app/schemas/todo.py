from pydantic import BaseModel
from typing import List, Optional


class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False


class Todo(TodoBase):
    id: str

    class Config:
        from_attributes = True


class TodoQuery(BaseModel):
    skip: int
    limit: int
    completed: Optional[bool] = None
    title: Optional[str] = None
    sort_by: Optional[str] = "title"
    sort_order: Optional[str] = "asc"


class TodoResponse(BaseModel):
    total: int
    data: List[Todo]

    class Config:
        from_attributes = True  # To read data from ORM models


class TodoUpdate(BaseModel):
    title: Optional[str] = None  # Allow updating title, but it's optional
    description: Optional[str] = None
    completed: Optional[bool] = None  # Allow updating completion status

    class Config:
        from_attributes = True  # To read data from ORM models


class TodoCreate(TodoBase):
    pass
