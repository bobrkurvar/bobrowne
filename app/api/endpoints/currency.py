from sys import prefix

from fastapi import APIRouter, HTTPException, status
from pathlib import Path
from app.core.config import load_config
from app.core.security import getUserFromToken
from app.db.session import getConnectDep
from app.db.models.user import User
from app.utils import external_api

router = APIRouter()

router.include_router(
    external_api.router,
    prefix="/currency"
)

path = Path(r'C:\project1\.env')
conf = load_config(path)
api_key = conf.CURRENCY_API_KEY

@router.get('/exchange')
async def exchange(username: getUserFromToken, session: getConnectDep):
    user = await session.get(User, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="I don't know!")
