from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException,status
from app.hashing import Hash

def create_user(user, db:Session):
    user = user.dict()
    try:
        new_user = models.User(
            username=user["username"],
            password=Hash.hash_password(user["password"]),
            email=user["email"],
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error creating user {e}"
        )

def get_user(user_id,db:Session):
    user = db.query(models.User).filter(models.User.id == user_id ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id}"
        )
    return user

def delete_user(user_id,db:Session):
    user = db.query(models.User).filter(models.User.id == user_id )
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id} therefore is not eliminated"
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"response":"User deleted successfully!"}

def get_all_users(db:Session):
    data = db.query(models.User).all()
    return data

def update_user(user_id,updateUser,db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id )
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id}"
        )
    usuario.update(updateUser.dict( exclude_unset=True))
    db.commit()
    return {"response":"User updated successfully!"}