from fastapi import APIRouter, Depends
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


@router.get("/points/player/{player}", response_model=List[schemas.PointEvent], summary='point logs for a player')
def read_player(player: str, db: Session = Depends(get_db)):
    db_player = crud.get_points_by_player(db, player=player)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@router.get("/points/player/{player}/season/{season}", response_model=List[schemas.PointEvent], summary='point logs for a specific player and season combination')
def read_player_and_season(player: str, season: str, db: Session = Depends(get_db)):
    db_ps = crud.get_points_by_player_and_season(db, player=player, season=season)
    if db_ps is None:
        raise HTTPException(status_code=404, detail="Player and Season combination not found")
    return db_ps