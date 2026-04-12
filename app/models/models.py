from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import List
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    todo: Mapped[List["Todo"]] = relationship(back_populates="user")

class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True, index=True)
    todo_text: Mapped[str] = mapped_column(String, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="todo")