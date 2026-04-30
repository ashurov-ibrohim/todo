from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_service import create_user_service, login, refresh_service, logout_service
from app.schemas.user_schemas import UserCreate, UserRead, UserLogin
from app.schemas.token_schemas import TokenResponse, RefreshRequests
from app.auth.dependencies import get_db, oauth2_scheme
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login_router(user_data: UserLogin, db: Session = Depends(get_db)):
    return login(db, user_data)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequests):
    return refresh_service(data.refresh_token)

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    return logout_service(token)