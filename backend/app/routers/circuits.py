from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Circuit
from app.schemas.circuits import CircuitInput, CircuitResponse

router = APIRouter()

@router.post("", response_model=CircuitResponse)
@router.post("/", response_model=CircuitResponse)
def create_circuit(circuit_data: CircuitInput, db: Session = Depends(get_db)):
    new_circuit = Circuit(
        name=circuit_data.name,
        country=circuit_data.country,
        city=circuit_data.city,
        lap_length_km=circuit_data.lap_length_km,
        total_turns=circuit_data.total_turns,
        lap_record_time=circuit_data.lap_record_time,
        lap_record_year=circuit_data.lap_record_year,
        drs_zones=circuit_data.drs_zones
    )
    db.add(new_circuit)
    db.commit()
    db.refresh(new_circuit)
    return new_circuit

@router.get("", response_model=list[CircuitResponse])
@router.get("/", response_model=list[CircuitResponse])
def get_circuits(
    db: Session = Depends(get_db),
    country: str = None
):
    query = db.query(Circuit)
    if country:
        query = query.filter(Circuit.country == country)
    return query.all()

@router.get("/{circuit_id}", response_model=CircuitResponse)
def get_circuit(circuit_id: int, db: Session = Depends(get_db)):
    circuit = db.query(Circuit).filter(Circuit.id == circuit_id).first()
    if circuit is None:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.get("/{circuit_id}/races", response_model=None)
def get_circuit_races(circuit_id: int, db: Session = Depends(get_db)):
    circuit = db.query(Circuit).filter(Circuit.id == circuit_id).first()
    if circuit is None:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return {
        "circuit": circuit.name,
        "country": circuit.country,
        "races": [
            {
                "id": race.id,
                "name": race.name,
                "date": str(race.date),
                "season": race.season.year
            }
            for race in circuit.races
        ]
    }