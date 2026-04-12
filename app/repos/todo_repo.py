from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.models.models import Todo
from app.schemas.todo_schemas import TodoCreate, TodoUpdate
from app.auth.user import get_current_user, get_db


def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_available = (
        db.query(Todo)
        .filter(
            (Todo.todo_text == todo_data.todo_text)
            & ((Todo.user_id) == (current_user.id))
        )
        .first()
    )

    if is_available is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This todo already exists",
        )

    todo = Todo(
        todo_text=todo_data.todo_text,
        is_completed=todo_data.is_completed,
        user_id=current_user.id,
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def get_todo(
    limit,
    offset,
    is_completed: bool,
    search: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    ic_filtered: bool = None

    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    if is_completed is not None:
        if is_completed:
            query = query.filter(Todo.is_completed == True)
            ic_filtered = True
        else:
            query = query.filter(Todo.is_completed == False)
            ic_filtered = False

    if search is not None:
        if ic_filtered:
            query = query.filter(
                (Todo.is_completed == True) & (Todo.todo_text == search)
            )
        elif ic_filtered is None:
            query = query.filter(Todo.todo_text == search)
        elif ic_filtered == False:
            query = query.filter((Todo.is_completed == False) & (Todo.todo_text == search))

    todo = query.order_by(Todo.id.asc()).limit(limit).offset(offset).all()

    if len(todo) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return todo


def delete_todo(
    todo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    todo = (
        db.query(Todo)
        .filter((Todo.user_id == current_user.id) & (todo_id == Todo.id))
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return {"msg": "Todo deleted"}


def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter((Todo.user_id == current_user.id) & (Todo.id == todo_id))
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    if todo_data.todo_text is not None:
        todo.todo_text = todo_data.todo_text

    if todo_data.is_completed is not None:
        todo.is_completed = todo_data.is_completed

    db.commit()
    db.refresh(todo)

    return {"msg": "updated", "todo": todo}
