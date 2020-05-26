from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from .database import Base


class PointEvent(Base):
    __tablename__ = "point_log"

    id = Column(Integer, primary_key=True, index=True)
    player = Column(String)
    team = Column(String)
    season = Column(String)
    data_date = Column(Date)
    points = Column(Float)
