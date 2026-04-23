from app.models.models import Users
from sqlalchemy.orm import Session

def create_user(db: Session, user):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_username(db: Session, username):
    return db.query(Users).filter(Users.username==username).first()