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
    "/refugee/{refugee}",
    response_model=schemas.Refugee,
    summary="get refugee",
)
def read_refugee(refugee: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugee(db, refugee=refugee)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
