import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.api.schemas.user import UserInput
from app.core.config import load_config
from pathlib import Path
from datetime import timedelta, datetime, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
pwd_context = CryptContext(schemes=["bcrypt"])
path = Path(r'C:\project1\.env')
conf = load_config(path)
secret_key = conf.SECRET_KEY
algorithm = conf.ALGORITHM

def get_password_hash(plain_password: str) -> str:
    hash_password = pwd_context.hash(plain_password)
    return hash_password

def verify(plain_password: str, password_hash: Annotated[str, Depends(get_password_hash)]) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(key=secret_key, algorithm=algorithm, payload=to_encode)
    return token

def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithm)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username

getUserFromToken = Annotated[str, Depends(get_user_from_token)]