from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.endpoints import user, currency
import uvicorn
from app.db.session import create_table, drop_all
from app.api.endpoints.currency import manager
import logging
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import request_validation_exception_handler, global_exception_handler, custom_exception_handler
from app.exceptions.custom_errors import CustomException

logging.basicConfig(level= logging.INFO, filename='my_log.log', filemode='a')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    await manager.start()
    yield
    await drop_all()
    await manager.close()

app = FastAPI(lifespan=lifespan)
app.include_router(
    user.router,
    prefix='/user'
)
app.include_router(
    currency.router,
    prefix='/currency'
)

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app)