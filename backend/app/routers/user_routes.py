from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.repository import user_service
from app.schemas.user import ShowUser, UpdateUser, UserCreate
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    current_users = user_service.get_all_users(db)
    return current_users


@router.post("/")
def create_new_user(new_user: UserCreate, db: Session = Depends(get_db)):
    user_service.create_user(new_user, db)
    return {"response": "User created successfully!"}


@router.get("/{user_id}", response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_found = user_service.get_user(user_id, db)
    return user_found


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = user_service.delete_user(user_id, db)
    return response


@router.patch("/{user_id}")
def update_user(user_id: int, updateUser: UpdateUser, db: Session = Depends(get_db)):
    response = user_service.update_user(user_id, updateUser, db)
    return response
