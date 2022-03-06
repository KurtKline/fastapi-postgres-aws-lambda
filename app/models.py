from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from .database import Base


class PointEvent(Base):
    __tablename__ = "point_log"

    id = Column(Integer, primary_key=True, index=True)
    player = Column(String(50))
    team = Column(String(50))
    season = Column(String(50))
    data_date = Column(Date)
    points = Column(Float)

class Refugee(Base):
    __tablename__ = "refugee"

    id = Column(Integer, primary_key=True, index=True)
    given_name = Column(String(50))
    family_name = Column(String(50))
    birth_date = Column(Date)
    salary_targeted = Column(Integer)

