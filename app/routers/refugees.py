from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List
import os

router = APIRouter()

# models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    # db = SessionLocal()
    try:
        yield None
    finally:
        pass
        # db.close()


@router.get(
    "/refugee/{refugee}",
    summary="get refugee",
)
def read_refugee(refugee: int, db: Session = Depends(get_db)):
    # db_refugee = crud.get_refugee(db, refugee=refugee)
    db_refugee = os.listdir(path=os.getcwd()) + ["TOTOT"] + \
    os.listdir(path=os.join(os.getcwd(), os.pardir)) + ["TOTOT"] + \
    os.listdir(path=os.join(os.join(os.getcwd(), os.pardir), os.pardir))
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
