from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Driver, Team
from app.schemas.drivers import DriverInput, DriverResponse

router = APIRouter()

@router.post("/",response_model=DriverResponse)
def create_driver(driver_data: DriverInput, db: Session = Depends(get_db)):
    if driver_data.team_id:
        team = db.query(Team).filter(Team.id == driver_data.team_id).first()
        if team is None:
            raise HTTPException(status_code=404, detail="Team not found")
    new_driver = Driver(
        first_name=driver_data.first_name,
        last_name=driver_data.last_name,
        nationality=driver_data.nationality,
        date_of_birth=driver_data.date_of_birth,
        driver_number=driver_data.driver_number,
        abbreviation=driver_data.abbreviation,
        team_id=driver_data.team_id,
        is_active=driver_data.is_active,
        bio=driver_data.bio,
        total_races=driver_data.total_races,
        total_wins=driver_data.total_wins,
        total_podiums=driver_data.total_podiums,
        total_poles=driver_data.total_poles,
        total_points=driver_data.total_points,
        total_championships=driver_data.total_championships
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

@router.get("/",response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db),team_id: int = None,nationality: str = None,is_active: bool = None):
    drivers = db.query(Driver)
    if team_id is not None:
        drivers = drivers.filter(Driver.team_id == team_id)
    if nationality:
        drivers = drivers.filter(Driver.nationality == nationality)
    if is_active is not None:
        drivers = drivers.filter(Driver.is_active == is_active)
    return drivers.all()

#Actual SQL Query for the above filter would look like this:
# SELECT * FROM drivers
# WHERE team_id = 1
# AND nationality = 'British'
# AND is_active = true

@router.get("/{driver_id}",response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver



@router.get("/{driver_id}/team",response_model=None)
def get_driver_with_team(driver_id:int, db:Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code = 404, detail = "Driver not found")
    return {
        "id":driver.id,
        "name":f"{driver.first_name} {driver.last_name}",
        "abbreviation":driver.abbreviation,
        "number":driver.driver_number,
        "nationality":driver.nationality,
        "team":{
            "id": driver.team.id,
            "name": driver.team.name,
            "nationality": driver.team.nationality,
            "primary_color": driver.team.primary_color
        }  if driver.team else None
    }

#Actual SQL Query for the above filter would look like this:
# SELECT drivers.*, team.*
# From drivers LEft Join teams ON drivers.team_id = teams.id
# Where drivers.id=1