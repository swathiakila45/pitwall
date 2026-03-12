from pydantic import BaseModel
from datetime import date as Date

class RaceInput(BaseModel):
    season_id: int
    circuit_id: int
    round: int
    name: str
    date: Date = None
    has_sprint: bool = False

class RaceResponse(BaseModel):
    id: int
    season_id: int
    circuit_id: int
    round: int
    name: str
    date: Date = None
    has_sprint: bool = False

    class Config:
        from_attributes = True