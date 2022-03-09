from fastapi import FastAPI
from .routers import players, teams, seasons, refugees

from mangum import Mangum

app = FastAPI(
    title="Robota Express API",
    # openapi_prefix="/prod"
)

app.include_router(players.router, tags=["Players"])
app.include_router(teams.router, tags=["Teams"])
app.include_router(seasons.router, tags=["Seasons"])
app.include_router(refugees.router, tags=["Seasons"])

handler = Mangum(app, lifespan="off")
