from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import user, currency
import uvicorn
from app.db.session import create_table, drop_all

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    await drop_all()

app = FastAPI(lifespan=lifespan)
app.include_router(
    user.router,
    prefix='/user'
)
app.include_router(
    currency.router,
    prefix='/currency'
)

if __name__ == "__main__":
    uvicorn.run(app)