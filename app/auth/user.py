from app.db.database import SessionLocal
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.models import Users, Todo
from app.security.security import SECRET_KEY, ALGORITHM
from uuid import UUID

oatuh2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db()-> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oatuh2_scheme), db: Session = Depends(get_db)):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: UUID = payload.get("sub")

        if user_id is None:
            raise auth_exception
    except JWTError:
        raise auth_exception
    
    user = db.query(Users).filter(Users.id==user_id).first()

    return user
