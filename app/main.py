from fastapi import FastAPI
from .routers import players, teams, seasons

from mangum import Mangum

app = FastAPI(
    title='FastAPI-AWS-Lambda-Test',
    openapi_prefix="/prod" # when deploying to prod
)

app.include_router(players.router, tags=["players"])
app.include_router(teams.router, tags=["teams"])
app.include_router(seasons.router, tags=["seasons"])

handler = Mangum(app, enable_lifespan=False)
