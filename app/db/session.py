from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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

async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

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

userFetchFromQueryDep = Annotated[User | None, Depends(user_fetch_from_query)]

async def user_fetch_from_form(user_form: Annotated[OAuth2PasswordRequestForm, Depends()], session: getConnectDep):
    hash_password = get_password_hash(user_form.password)
    query = (
        select(User).where(
            (User.username == user_form.username) &
            (User.password == hash_password)
        )
    )
    result = await session.execute(query)
    return result.scalars().first()
userFetchFromFormDep = Annotated[User | None, Depends(user_fetch_from_form)]