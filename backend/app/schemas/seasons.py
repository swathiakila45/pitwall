from pydantic import BaseModel

class SeasonInput(BaseModel):
    year: int

class SeasonResponse(BaseModel):
    id: int
    year: int

    class Config:
        from_attributes = True