from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_service import create_user_service, login, refresh_service, logout_service
from app.schemas.user_schemas import UserCreate, UserRead
from app.schemas.token_schemas import TokenResponse, RefreshRequests
from app.auth.user import get_db, get_current_user, oatuh2_scheme
from jose import jwt
from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user_data)


@router.post("/login")
def login_router(user_data: UserCreate, db: Session = Depends(get_db)):
    return login(db, user_data)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequests):
    return refresh_service(data.refresh_token)

@router.post("/logout")
def logout(token: str = Depends(oatuh2_scheme)):
    return logout_service(token)