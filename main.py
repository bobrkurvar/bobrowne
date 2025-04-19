
from fastapi import FastAPI
from app.api.endpoints import user, currency
import uvicorn

app = FastAPI()
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