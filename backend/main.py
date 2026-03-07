from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from app.database import SessionLocal, engine 
from app.models.models import Base, Team 
from app.routers import teams


Base.metadata.create_all(bind=engine)

app= FastAPI()
app.include_router(teams.router, prefix="/teams", tags=["Teams"])

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



