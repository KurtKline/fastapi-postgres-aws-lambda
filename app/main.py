from fastapi import FastAPI
from .routers import refugees

from mangum import Mangum

app = FastAPI(
    title="Robota Express API",
    # openapi_prefix="/prod"
)

app.include_router(refugees.router, tags=["Seasons"])

handler = Mangum(app, lifespan="off")