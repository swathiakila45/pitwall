from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.models import Team
from app.schemas.teams import TeamInput, TeamResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_team(team_data: TeamInput,db:Session = Depends(get_db)):
    new_team = Team(
        name=team_data.name,
        nationality=team_data.nationality,
        base=team_data.base,
        team_principal=team_data.team_principal,
        championships=team_data.championships,
        is_active=team_data.is_active,
        primary_color=team_data.primary_color
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/", response_model=list[TeamResponse])
def get_teams(db:Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int,db:Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team