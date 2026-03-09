from pydantic import BaseModel
from datetime import date

class DriverInput(BaseModel):
    first_name:str
    last_name:str
    nationality:str=None
    date_of_birth:date=None
    driver_number:int = None
    abbreviation:str = None
    team_id:int = None
    is_active:bool = True
    bio:str = None
    total_races:int = 0
    total_wins:int = 0
    total_podiums:int = 0
    total_poles:int = 0
    total_points:float=0
    total_championships:int = 0

class DriverResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    nationality:str=None
    date_of_birth:date=None
    driver_number:int = None
    abbreviation:str = None
    team_id:int = None
    is_active:bool = True
    bio:str = None
    total_races:int = 0
    total_wins:int = 0
    total_podiums:int = 0
    total_poles:int = 0
    total_points:float=0
    total_championships:int = 0

class Config:
    from_attributes = True