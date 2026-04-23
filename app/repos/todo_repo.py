from sqlalchemy.orm import Session
from app.models.models import Todo


def create_todo(db: Session, todo):
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def check_existence(db: Session, user_id, todo_text):
    return db.query(Todo).filter((Todo.todo_text == todo_text) & (Todo.user_id == user_id)).first()
