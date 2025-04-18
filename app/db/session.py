from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy import select
from app.db.models.user import Base
from app.core.config import load_config
from pathlib import Path
from fastapi import Depends
from typing import Annotated
from app.db.models.user import User
from app.api.schemas.user import UserInput
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core.security import get_password_hash

path = Path(r'C:\project1\.env')
conf = load_config(path)
DB_URL = str(conf.DATABASE_URL)


async def get_connect():
    engine = create_async_engine(DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

async def user_insert(user: UserInput, engine: Annotated[AsyncEngine, Depends(get_connect)], password_hash: Annotated[str, Depends(get_password_hash)]):
    async_session = async_sessionmaker(engine)
    new_user = User(username= user.username, password=password_hash)
    async with async_session.begin() as session:
            session.add(new_user)

async def user_fetch_from_query(user: str, engine: Annotated[AsyncEngine,Depends(get_connect)]):
    async_session = async_sessionmaker(engine)
    async with async_session.begin() as session:
        result = await session.get(User, user)
        yield result


async def user_fetch_from_from(user_form: Annotated[OAuth2PasswordRequestForm, Depends()],  engine: Annotated[AsyncEngine,Depends(get_connect)]):
    async_session = async_sessionmaker(engine)
    async with async_session.begin() as session:
        result = await session.scalars(
            select(User).where(
                (User.username == user_form.username) &
                (User.password == user_form.password)
            )
        )
        yield result.first()
