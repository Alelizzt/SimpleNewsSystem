from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.token import verify_token
from app.core.config import settings

API_VERSION_PREFIX = f"/v{settings.PROJECT_VERSION.split('.')[0]}"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_VERSION_PREFIX}/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
