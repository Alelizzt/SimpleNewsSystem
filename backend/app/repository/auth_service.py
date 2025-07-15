from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from app.auth_token import create_access_token


def auth_user(user, db: Session):
    user_auth = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )

    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""The user with the username {user.username} does not exist, therefore the login is not performed.""",
        )

    if not Hash.verify_password(user.password, user_auth.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password !"
        )
    access_token = create_access_token(data={"sub": user.username, "id": user_auth.id})
    return {"access_token": access_token, "token_type": "bearer"}
