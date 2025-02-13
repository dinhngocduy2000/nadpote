from fastapi import FastAPI
from app.api.v1.endpoints.todo import router as todo_router
from app.database.session import engine, Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(todo_router, prefix="/api/v1")