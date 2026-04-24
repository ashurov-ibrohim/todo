from app.repos.todo_repo import (
    create_todo,
    check_existence,
    get_todos,
    update_todo,
    find_todo_by_id,
    delete_todo
)
from app.models.models import Todo
from app.schemas.todo_schemas import TodoCreate, TodoUpdate
from fastapi import HTTPException, status


def create_todo_service(db, user_id, todo_data: TodoCreate):
    if check_existence(db, user_id, todo_data.todo_text) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This todo already exists"
        )

    todo = Todo(
        todo_text=todo_data.todo_text,
        is_completed=todo_data.is_completed,
        user_id=user_id,
    )

    return create_todo(db, todo)


def get_todo_service(db, user_id):
    return get_todos(db, user_id)


def update_todo_service(db, user_id, todo_id, todo_data: TodoUpdate):
    todo_db = find_todo_by_id(db, user_id, todo_id)
    if not todo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    update_data = todo_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo_db, key, value)

    return update_todo(db, todo_db)

def delete_todo_service(db, user_id, todo_id):
    todo_db = find_todo_by_id(db, user_id, todo_id)

    if not todo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    delete_todo(db, todo_db)
    
