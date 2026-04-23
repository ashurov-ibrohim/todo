from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.models.models import Users
from app.core.security import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
from app.schemas.user_schemas import UserCreate, UserUpdateUsername, UserUpdatePassword
from app.auth.user import get_db, get_current_user


def create_user_query(db: Session, user_data: UserCreate):
    if db.query(Users).filter(user_data.username == Users.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username already exists",
        )

    user = Users(
        username=user_data.username, password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login(user_data, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == user_data.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this username not found",
        )

    if verify_password(user_data.password, user.password):
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
    )


def make_refresh_token(refresh_token):
    payload = verify_token(refresh_token)
    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="It's not refresh token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    access_token = create_access_token({"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}


def update_user(
    user_data: UserUpdateUsername,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(Users).filter(Users.id == current_user.id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    data = user_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def update_password(
    user_data: UserUpdatePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(Users).filter(Users.id == current_user.id).first()
