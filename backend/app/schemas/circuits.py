from pydantic import BaseModel

class CircuitInput(BaseModel):
    name: str 
    country: str = None
    city: str = None
    lap_length_km: float = None
    total_turns:int = None
    lap_record_time:str =None 
    lap_record_year:int = None
    drs_zones:int = None 

class CircuitResponse(BaseModel):
    id: int 
    name:str 
    country:str = None 
    city:str = None
    lap_length_time:float =None
    total_runs:int = None
    lap_record_time:str= None 
    lap_record_year:int = None 
    drs_zones : int = None 

class Config:
    from_attributes = True 

