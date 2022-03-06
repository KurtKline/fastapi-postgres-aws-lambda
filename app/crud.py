from sqlalchemy.orm import Session

from . import models, schemas

def get_refugee(db: Session, refugee: int = 0):
    return db.get(models.Refugee, refugee)

def get_point_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PointEvent).offset(skip).limit(limit).all()


def get_points_by_player(db: Session, player: str):
    return db.query(models.PointEvent).filter(models.PointEvent.player == player).all()


def get_points_by_team(db: Session, team: str):
    return db.query(models.PointEvent).filter(models.PointEvent.team == team).all()


def get_points_by_season(db: Session, season: str):
    return db.query(models.PointEvent).filter(models.PointEvent.season == season).all()


def get_points_by_team_and_season(db: Session, team: str, season: str):
    return (
        db.query(models.PointEvent)
        .filter(models.PointEvent.team == team, models.PointEvent.season == season)
        .all()
    )


def get_points_by_player_and_season(db: Session, player: str, season: str):
    return (
        db.query(models.PointEvent)
        .filter(models.PointEvent.player == player, models.PointEvent.season == season)
        .all()
    )
