from pydantic import BaseModel

class TeamInput(BaseModel):
    name: str
    nationality: str
    base: str = None
    team_principal: str = None
    championships: int = 0
    is_active: bool = True
    primary_color: str = None

class TeamResponse(BaseModel):
    id: int
    name: str
    nationality: str
    base: str = None
    team_principal: str = None
    championships: int = 0
    is_active: bool = True
    primary_color: str = None

    class Config:
        from_attributes = True