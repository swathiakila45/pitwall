from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Race, Season, Circuit
from app.schemas.races import RaceInput, RaceResponse

router = APIRouter()

@router.post("", response_model=RaceResponse)
@router.post("/", response_model=RaceResponse)
def create_race(race_data: RaceInput, db: Session = Depends(get_db)):
    # Validate season exists
    season = db.query(Season).filter(Season.id == race_data.season_id).first()
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    # Validate circuit exists
    circuit = db.query(Circuit).filter(Circuit.id == race_data.circuit_id).first()
    if circuit is None:
        raise HTTPException(status_code=404, detail="Circuit not found")

    new_race = Race(
        season_id=race_data.season_id,
        circuit_id=race_data.circuit_id,
        round=race_data.round,
        name=race_data.name,
        date=race_data.date,
        has_sprint=race_data.has_sprint
    )
    db.add(new_race)
    db.commit()
    db.refresh(new_race)
    return new_race

@router.get("", response_model=None)
@router.get("/", response_model=None)
def get_races(
    db: Session = Depends(get_db),
    season_id: int = None,
    circuit_id: int = None
):
    query = db.query(Race)
    if season_id:
        query = query.filter(Race.season_id == season_id)
    if circuit_id:
        query = query.filter(Race.circuit_id == circuit_id)

    races = query.order_by(Race.round).all()

    return [
        {
            "id": race.id,
            "name": race.name,
            "round": race.round,
            "date": str(race.date),
            "season": race.season.year,
            "circuit": race.circuit.name,
            "country": race.circuit.country,
            "has_sprint": race.has_sprint
        }
        for race in races
    ]

@router.get("/{race_id}", response_model=None)
def get_race(race_id: int, db: Session = Depends(get_db)):
    race = db.query(Race).filter(Race.id == race_id).first()
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")

    return {
        "id": race.id,
        "name": race.name,
        "round": race.round,
        "date": str(race.date),
        "has_sprint": race.has_sprint,
        "season": {
            "id": race.season.id,
            "year": race.season.year
        },
        "circuit": {
            "id": race.circuit.id,
            "name": race.circuit.name,
            "country": race.circuit.country,
            "city": race.circuit.city,
            "lap_length_km": race.circuit.lap_length_km
        }
    }