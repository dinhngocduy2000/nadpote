from typing import Optional
from fastapi import Query
from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from sqlalchemy import asc, desc

#  get a single todo
def get_todo(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()


# get list of todos
def get_todos(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = Query(None),
    title: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("title"),
    sort_order: Optional[str] = Query("asc"),
):
    # Define sorting map for fields
    sort_field_map = {
        "id": Todo.id,
        "title": Todo.title,
        "completed": Todo.completed
    }
    sort_field = sort_field_map.get(sort_by,Todo.title)

    query = db.query(Todo)
    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if title is not None:
        query = query.filter(Todo.title.ilike(f"%{title}%"))

    if sort_order =="asc":
        query = query.order_by(asc(sort_field))
    else:
        query = query.order_by(desc(sort_field))
    

    return query.filter(Todo.user_id == user_id).offset(skip).limit(limit).all()


# create a todo
def create_todo(db: Session, todo: TodoCreate, user_id: int):
    db_todo = Todo(**todo.dict(), user_id=user_id)  # Assign user ID
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# update a todo
def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if db_todo:
        for key, value in todo_update.dict().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


# delete a todo
def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
