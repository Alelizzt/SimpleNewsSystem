from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.login import LoginUser
from app.repository import auth_service

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post('/', status_code=status.HTTP_200_OK)
def login_user(user:LoginUser, db:Session = Depends(get_db)):
    auth_token = auth_service.auth_user(user, db)
    return auth_token