from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash


def create_user(user, db: Session):
    try:
        # Validar campos obligatorios
        if not user.username or not user.email or not user.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username, email, and password are required fields"
            )

        # Validar si el correo ya está registrado
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A user with this email already exists"
            )

        # Crear el usuario
        new_user = models.User(
            username=user.username,
            password=Hash.hash_password(user.password),
            email=user.email,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )


def get_user(user_id, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id}",
        )
    return user


def delete_user(user_id, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id} therefore is not eliminated",
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"response": "User deleted successfully!"}


def get_all_users(db: Session):
    data = db.query(models.User).all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return data


def update_user(user_id, updateUser, db: Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the id {user_id}",
        )
    usuario.update(updateUser.model_dump(exclude_unset=True))
    db.commit()
    return {"response": "User updated successfully!"}
