from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.core.config import settings

pw_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# def create_token(data:dict, type: str):
#     to_encode = data.copy()

#     expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) if type=="refresh" else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def verify_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != expected_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
            )
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def verify_access_token(token: str):
    return verify_token(token, "access")

def verify_refresh_token(token: str):
    return verify_token(token, "refresh")

def hash_password(password: str) -> str:
    return pw_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pw_context.verify(plain_password, hashed_password)
