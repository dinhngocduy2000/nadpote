from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.schemas import User
from app.auth.services import get_current_active_user
from app.schemas.todo import Todo, TodoCreate, TodoUpdate
from app.crud.todo import get_todos, create_todo, get_todo, update_todo, delete_todo
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
    current_user: User = Depends(get_current_active_user)
):
    return create_todo(db, todo)

@router.get("/todos/", response_model=list[Todo])
def read_todos(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    return get_todos(db, skip, limit)

@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo_endpoint(
    todo_id: int, 
    todo_update: TodoUpdate,  # Use a request body instead of a query param
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_todo = update_todo(db, todo_id, todo_update)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo_endpoint(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_todo = delete_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
