from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.auth.services import get_current_active_user
from app.models.user import User
from app.schemas.todo import Todo, TodoCreate, TodoUpdate, TodoResponse, TodoQuery
from app.crud.todo import get_todos, create_todo, get_todo, update_todo, delete_todo, count_todos
from app.database.session import SessionLocal

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/todos/", response_model=Todo)
def create_todo_endpoint(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_todo(db, todo, current_user.id)


@router.get("/todos/", response_model=TodoResponse)
def read_todos(
    input: TodoQuery = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    data = get_todos(db, current_user.id, input)
    total = count_todos(db, current_user.id, input)
    return TodoResponse(total=total, data=data)


@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_todo = get_todo(db, todo_id, current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/todos/{todo_id}", response_model=Optional[Todo])
def update_todo_endpoint(
    todo_id: str,
    todo_update: TodoUpdate,  # Use TodoUpdate schema here
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Optional[Todo]:
    db_todo = update_todo(db, todo_id, todo_update, current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo_endpoint(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_todo = delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
