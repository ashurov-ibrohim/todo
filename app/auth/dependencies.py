from app.db.database import SessionLocal
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.models import Users
from app.core.config import settings
from uuid import UUID
from app.core.blacklist import blacklisted_tokens
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token in blacklisted_tokens:
        raise auth_exception

    payload = verify_token(token, "access")
    user_id: UUID = payload.get("sub")

    if not user_id:
        raise auth_exception
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise auth_exception
    return user
