from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    userame: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    userame: str = None
    email: EmailStr = None
    password: str = None

class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config():
        from_attributes = True # orm_mode