from fastapi import APIRouter, Depends
from app.schemas.todo_schemas import TodoCreate, TodoRead
from app.auth.user import get_current_user, get_db
from app.services.todo_service import create_todo_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todo", tags=["TODO"])

@router.post("/post", response_model=TodoRead)
def create_todo(todo_data: TodoCreate, db: Session =  Depends(get_db), current_user = Depends(get_current_user)):
    return create_todo_service(db, current_user.id, todo_data)