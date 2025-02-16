from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from app.api.v1.endpoints.todo import router as todo_router
from app.database.session import engine, Base
from app.api.v1.endpoints.auth import router as auth_router

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create the database tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(todo_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")