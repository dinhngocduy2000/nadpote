from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database.session import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Link to User
    description=Column(String, index=True)
     # Relationship to the User model
    user = relationship("User", back_populates="todos")
