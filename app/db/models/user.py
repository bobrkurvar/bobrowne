from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "Users"
    username: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column()

