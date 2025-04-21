from fastapi import APIRouter, HTTPException, status, Query, Depends
from fastapi.responses import JSONResponse
from app.core.security import getUserFromToken
from app.db.session import getConnectDep
from app.db.models.user import User
from typing import Annotated
from app.utils.external_api import ExternalAPI
from app.core.config import load_config
from pathlib import Path

path = Path(r'C:\project1\.env')
conf = load_config(path)
ex_api_url = conf.EXTERNAL_API_URL

router = APIRouter(dependencies=[Depends(ExternalAPI)])



manager = ExternalAPI(ex_api_url)

@router.get('/exchange', response_class=JSONResponse)
async def exchange(username: getUserFromToken, session: getConnectDep,
                   to: Annotated[str, Query(max_length=3, min_length=3)], off: Annotated[str, Query(max_length=3, min_length=3)],
                   amount: int):
    user = await session.get(User, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="I don't know!")
    return await manager.convert(amount=amount, to=to, _from=off)

@router.get('/list', response_class=JSONResponse)
async def currencies_list():
    return await manager.cur_list

