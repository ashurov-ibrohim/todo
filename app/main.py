from fastapi import FastAPI, Depends, status
from app.repos.user_repo import create_user_query, login, update_user
from app.repos.todo_repo import create_todo, get_todo, delete_todo, update_todo
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserRead, UserCreate, LoginRead, UserUpdateUsername, UserOut
from app.schemas.todo_schemas import TodoCreate, TodoRead, TodoUpdate
from app.auth.user import get_current_user, get_db

app = FastAPI()

@app.post("/signup", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user_query(db, user_data)


@app.post("/login", response_model=LoginRead)
def log_in(user_data: UserCreate, db: Session = Depends(get_db)):
    return login(user_data, db)

@app.patch("/newusername", response_model=UserOut)
def update_username(user_data: UserUpdateUsername, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return update_user(user_data, db, current_user)


@app.post("/todo", response_model=TodoRead)
def post_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_todo(todo_data, db, current_user)


@app.get("/todo", response_model=list[TodoRead])
def get_todo_endpoint(
    limit=10,
    offset=0,
    is_completed: bool = None,
    search: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_todo(limit, offset, is_completed, search, db, current_user)


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return delete_todo(id, db, current_user)


@app.patch("/todo/{id}", response_model=TodoRead)
def patch_todo(
    id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_todo(id, todo_data, db, current_user)
