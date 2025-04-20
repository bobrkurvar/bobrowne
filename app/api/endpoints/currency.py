from fastapi import APIRouter, HTTPException, status
from app.core.security import getUserFromToken
from app.db.session import getConnectDep
from app.db.models.user import User

router = APIRouter()

@router.get('/exchange')
async def exchange(username: getUserFromToken, session: getConnectDep):
    user = await session.get(User, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="I don't know!")
