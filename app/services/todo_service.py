from app.repos.todo_repo import create_todo, check_existence
from app.models.models import Todo
from app.schemas.todo_schemas import TodoCreate
from fastapi import HTTPException, status

def create_todo_service(db, user_id ,todo_data: TodoCreate):
    if check_existence(db, user_id, todo_data.todo_text) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This todo already exists")

    todo = Todo(
        todo_text=todo_data.todo_text,
        is_completed=todo_data.is_completed,
        user_id=user_id
    )

    return create_todo(db, todo)