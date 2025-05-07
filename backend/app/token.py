from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.schemas.login import TokenData

# Para generar una clave secreta aleatoria, puedes usar el siguiente comando:
# openssl rand -hex 32
SECRET_KEY = "de3f432731c1efdc6b7caa0b83e50b61a59435a653c04c7ead1eebd78b662bab"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        if not token_data:
            raise credentials_exception
        return True
    except JWTError:
        raise credentials_exception