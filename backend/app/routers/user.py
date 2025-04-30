from fastapi import APIRouter

from app.schemas.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_all_users():
    return {"message": "Get all users"}

@router.post("/")
def create_user(user: User):
    print(user)
    return True

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"Get user with id {user_id}"}

@router.delete("/{user_id}")
def delete_user(user_id:int):
    return True

@router.patch('/{user_id}')
def update_user(user_id:int, updateUser:User,):
    #update_user(user_id,updateUser)
    return True
