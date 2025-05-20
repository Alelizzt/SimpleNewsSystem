from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "username": "juanperez",
                "email": "juan@example.com",
                "password": "supersecret",
                "created_at": "2024-05-19T12:00:00"
            }
        }

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "juanperez",
                "email": "juan@example.com",
                "password": "supersecret"
            }
        }

class UpdateUser(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "nuevo_nombre",
                "email": "nuevo@email.com",
                "password": "nuevaclave"
            }
        }

class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # orm_mode
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "juanperez",
                "email": "juan@example.com"
            }
        }