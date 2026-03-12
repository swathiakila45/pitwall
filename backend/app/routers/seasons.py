from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Season
from app.schemas.seasons import SeasonInput, SeasonResponse

router = APIRouter()

@router.post("", response_model=SeasonResponse)
@router.post("/", response_model=SeasonResponse)
def create_season(season_data: SeasonInput, db: Session = Depends(get_db)):
    existing = db.query(Season).filter(Season.year == season_data.year).first()
    if existing:
        raise HTTPException(status_code=400, detail="Season already exists")
    new_season = Season(year=season_data.year)
    db.add(new_season)
    db.commit()
    db.refresh(new_season)
    return new_season

@router.get("", response_model=list[SeasonResponse])
@router.get("/", response_model=list[SeasonResponse])
def get_seasons(db: Session = Depends(get_db)):
    return db.query(Season).order_by(Season.year.desc()).all()

@router.get("/{season_id}", response_model=None)
def get_season(season_id: int, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id).first()
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return {
        "id": season.id,
        "year": season.year,
        "races": [
            {
                "id": race.id,
                "name": race.name,
                "round": race.round,
                "date": str(race.date),
                "circuit": race.circuit.name
            }
            for race in season.races
        ]
    }