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


@router.get("/points/season/{season}", response_model=List[schemas.PointEvent], summary='point logs for a season')
def read_season(season: str, db: Session = Depends(get_db)):
    db_season = crud.get_points_by_season(db, season=season)
    if db_season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return db_season