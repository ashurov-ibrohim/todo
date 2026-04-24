from fastapi import APIRouter, Depends
from app.schemas.todo_schemas import TodoCreate, TodoRead, TodoUpdate
from app.auth.user import get_current_user, get_db
from app.services.todo_service import (
    create_todo_service,
    get_todo_service,
    update_todo_service,
    delete_todo_service,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todo", tags=["TODO"])


@router.post("/post", response_model=TodoRead)
def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_todo_service(db, current_user.id, todo_data)


@router.get("/", response_model=list[TodoRead])
def get_todos(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_todo_service(db, current_user.id)


@router.patch("/{todo_id}")
def update_todo(
    todo_data: TodoUpdate,
    todo_id,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_todo_service(db, current_user.id, todo_id, todo_data)


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    delete_todo_service(db, current_user.id, todo_id)

    return {"message": "deleted"}