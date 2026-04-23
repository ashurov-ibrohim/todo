from sqlalchemy.orm import Session
from app.repos.user_repo import get_user_by_username, create_user
from fastapi import HTTPException, status
from app.models.models import Users
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.schemas.user_schemas import UserCreate
from app.core.blacklist import blacklisted_tokens


def create_user_service(db: Session, user: UserCreate):
    if get_user_by_username(db, user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This user already exists"
        )

    user_obj = Users(username=user.username, password=hash_password(user.password))

    return create_user(db, user_obj)


def login(db: Session, user_data: UserCreate):
    user_db = get_user_by_username(db, user_data.username)

    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(user_data.password, user_db.password):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = create_access_token({"sub": str(user_db.id)})
    refresh_token = create_refresh_token({"sub": str(user_db.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_service(token):
    payload = verify_token(token, "refresh")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    new_access_token = create_access_token({"sub": str(user_id)})

    return {"access_token": new_access_token, "token_type": "bearer"}

def logout_service(token: str):

    verify_token(token, expected_type="access")

    blacklisted_tokens.add(token)

    return {"message": "Successfully logged out"}
