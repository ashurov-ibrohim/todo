from sqlalchemy.orm import Session
from app.models.models import Todo


def create_todo(db: Session, todo):
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


def check_existence(db: Session, user_id, todo_text):
    return (
        db.query(Todo)
        .filter((Todo.todo_text == todo_text) & (Todo.user_id == user_id))
        .first()
    )


def get_todos(db: Session, user_id):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def find_todo_by_id(db, user_id, todo_id):
    return db.query(Todo).filter(Todo.user_id == user_id, Todo.id == todo_id).first()

def update_todo(db: Session, todo):
    db.commit()
    db.refresh(todo)

    return todo

def delete_todo(db: Session, todo):
    db.delete(todo)
    db.commit()