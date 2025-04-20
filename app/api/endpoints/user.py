from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.token import Token
from app.api.schemas.user import UserInput, UserOutput
from app.db.session import user_insert, userFetchFromQueryDep,userFetchFromFormDep
from app.core.security import create_token
from app.core.config import load_config
from pathlib import Path
from datetime import timedelta



router = APIRouter()

path = Path(r'C:\project1\.env')
conf = load_config(path)
access_token_expire_minutes = conf.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post('/register')
async def register(user: UserInput):
    await user_insert(user)
    return UserOutput(username= user.username)

@router.get('/')
async def fetch(result: userFetchFromQueryDep):
    return result.username, result.password if result else "Not found"

@router.post('/token')
async def login(result: userFetchFromFormDep):
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data_dict = {'sub': result.username}
    expires_delta = timedelta(minutes=access_token_expire_minutes)
    token = create_token(data_dict, expires_delta)
    return Token(access_token=token, token_type="bearer")





