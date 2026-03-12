from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from app.database import SessionLocal, engine 
from app.models.models import Base, Team 
from app.routers import teams, drivers,circuits, seasons,races


Base.metadata.create_all(bind=engine)

app= FastAPI(redirect_slashes=False)
app.include_router(teams.router,    prefix="/teams",    tags=["Teams"])
app.include_router(drivers.router,  prefix="/drivers",  tags=["Drivers"])
app.include_router(circuits.router, prefix="/circuits", tags=["Circuits"])
app.include_router(seasons.router,  prefix="/seasons",  tags=["Seasons"])
app.include_router(races.router, prefix = "/races", tags=["Races"])
class TeamInput(BaseModel):
    name:str
    nationality:str
    is_active:bool = True 


#  Define a route for the home page
@app.get("/")
def home():
    return {"message": "Pit wall APi is running"} 

#Define the route for driver's data by name 

@app.get("/drivers/{driver_name}")
def getDriver(driver_name:str):
    return {"driver":driver_name}

class Driver(BaseModel):
    name:str
    team:str
    number:int 
    nationality:str 

@app.get("/driver-info")
def get_driver_info():
    return Driver(
        name="Kimi Antonelli",
        team="Mercedes-AMG Petronas Formula One Team",
        number=12,
        nationality = "Italian"
    )

@app.post("/drivers/add")
def add_driver(driver:Driver):
    return {
        "message":f"Driver {driver.name} added successfully",
        "data": driver
    }



