from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.models import Team
from app.schemas.teams import TeamInput, TeamResponse

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_team(team_data: TeamInput):
    db = SessionLocal()
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
    db.close()
    return new_team

@router.get("/", response_model=list[TeamResponse])
def get_teams():
    db = SessionLocal()
    teams = db.query(Team).all()
    db.close()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int):
    db = SessionLocal()
    team = db.query(Team).filter(Team.id == team_id).first()
    db.close()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team