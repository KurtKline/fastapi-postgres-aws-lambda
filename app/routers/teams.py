from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/points/team/{team}",
    response_model=List[schemas.PointEvent],
    summary="point logs for a team",
)
def read_team(team: str, db: Session = Depends(get_db)):
    db_team = crud.get_points_by_team(db, team=team)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.get(
    "/points/team/{team}/season/{season}",
    response_model=List[schemas.PointEvent],
    summary="point logs for a specific team and season combination",
)
def read_team_and_season(team: str, season: str, db: Session = Depends(get_db)):
    db_ts = crud.get_points_by_team_and_season(db, team=team, season=season)
    if db_ts is None:
        raise HTTPException(
            status_code=404, detail="Team and Season combination not found"
        )
    return db_ts
