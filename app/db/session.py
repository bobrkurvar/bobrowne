from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy import select
from app.db.models.user import Base
from app.core.config import load_config
from pathlib import Path
from fastapi import Depends
from typing import Annotated, Any
from app.db.models.user import User
from app.api.schemas.user import UserInput
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core.security import get_password_hash

path = Path(r'C:\project1\.env')
conf = load_config(path)
DB_URL = str(conf.DATABASE_URL)
engine = create_async_engine(DB_URL)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_connect():
    async_session = async_sessionmaker(engine)
    async with async_session.begin() as session:
        yield session

getConnectDep = Annotated[Any, Depends(get_connect)]

async def user_insert(user: UserInput, session: getConnectDep, password_hash: Annotated[str, Depends(get_password_hash)]):
    new_user = User(username= user.username, password=password_hash)
    session.add(new_user)

async def user_fetch_from_query(user: str, session: getConnectDep):
    result = await session.get(User, user)
    return result


async def user_fetch_from_from(user_form: Annotated[OAuth2PasswordRequestForm, Depends()],  session: getConnectDep):
    query = (
        select(User).where(
            (User.username == user_form.username) &
            (User.password == user_form.password)
        )
    )
    result = session.execute(query)
    return result.scalars().first()
