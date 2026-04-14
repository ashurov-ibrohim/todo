from pydantic import BaseModel, constr

class UserRead(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=30)
    password: constr(min_length=5, max_length=50)

    class Config:
        orm_mode = True

class LoginRead(BaseModel):
    access_token: str
    token_type: str