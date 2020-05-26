from fastapi import FastAPI
from .routers import players, teams, seasons

from mangum import Mangum

app = FastAPI(
    title="FastAPI-PostgreSQL-AWS-Lambda",
    # openapi_prefix="/prod"
)

app.include_router(players.router, tags=["Players"])
app.include_router(teams.router, tags=["Teams"])
app.include_router(seasons.router, tags=["Seasons"])

handler = Mangum(app, enable_lifespan=False)
