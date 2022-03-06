from typing import List, Optional
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

class Refugee(BaseModel):
    id: int
    given_name: str
    family_name: str
    birth_date: Optional[date] = None
    salary_targeted: Optional[int] = None

    class Config:
        orm_mode = True
