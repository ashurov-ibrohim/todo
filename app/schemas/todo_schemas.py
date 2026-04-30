from pydantic import BaseModel, constr
from typing import Optional


class TodoRead(BaseModel):
    todo_text: str
    is_completed: bool

    model_config = {"from_attributes": True}


class TodoCreate(BaseModel):
    todo_text: constr(min_length=3, max_length=200)
    is_completed: bool
    
    model_config = {"from_attributes": True}


class TodoUpdate(BaseModel):
    todo_text: Optional[constr(min_length=3, max_length=200)] = None
    is_completed: Optional[bool] = None
