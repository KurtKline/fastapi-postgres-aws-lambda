from typing import List
from pydantic import BaseModel
from datetime import date


class PointEvent(BaseModel):
    id: int
    player: str
    team: str
    season: str
    data_date: date
    points: float

    class Config:
        orm_mode = True
