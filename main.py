from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.api.endpoints import user, currency
from fastapi.encoders import jsonable_encoder
import uvicorn
from app.db.session import create_table, drop_all
import logging
from app.api.schemas.exception import CustomExceptionModel

logging.basicConfig(level= logging.INFO, filename='my_log.log', filemode='a')

class CustomException(HTTPException):
    def __init__(self, message: str, detail: str, status_code: int = 400):
        HTTPException.__init__(self, status_code, detail)
        self.message = message

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

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    error = jsonable_encoder(CustomExceptionModel(status_code=exc.status_code,
                                                  er_message=exc.message,
                                                  er_details=exc.detail))
    logging.exception(error.message)
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.exception("Internal server error")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(app)