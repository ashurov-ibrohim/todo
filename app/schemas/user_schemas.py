from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID

class UserRead(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=30)
    password: constr(min_length=8, max_length=255)

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: constr(min_length=5, max_length=30)
    password: constr(min_length=8, max_length=255)

class LoginRead(BaseModel):
    access_token: str
    token_type: str

class UserUpdateUsername(BaseModel):
    username: Optional[constr(min_length=5, max_length=30)] = None

class UserUpdatePassword(BaseModel):
    old_password: constr(min_length=8, max_length=255)
    new_password: constr(min_length=8, max_length=255)


class UserOut(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True
