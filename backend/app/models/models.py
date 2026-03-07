from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    nationality     = Column(String)
    base            = Column(String)
    team_principal  = Column(String)
    championships   = Column(Integer, default=0)
    is_active       = Column(Boolean, default=True)
    primary_color   = Column(String)

    drivers  = relationship("Driver", back_populates="team")
    results  = relationship("Result", back_populates="team")


class Driver(Base):
    __tablename__ = "drivers"

    id              = Column(Integer, primary_key=True)
    first_name      = Column(String, nullable=False)
    last_name       = Column(String, nullable=False)
    nationality     = Column(String)
    date_of_birth   = Column(Date)
    driver_number   = Column(Integer)
    abbreviation    = Column(String(3))
    team_id         = Column(Integer, ForeignKey("teams.id"))
    is_active       = Column(Boolean, default=True)
    bio             = Column(Text)

    # Career totals
    total_races         = Column(Integer, default=0)
    total_wins          = Column(Integer, default=0)
    total_podiums       = Column(Integer, default=0)
    total_poles         = Column(Integer, default=0)
    total_points        = Column(Float, default=0)
    total_championships = Column(Integer, default=0)

    team     = relationship("Team", back_populates="drivers")
    results  = relationship("Result", back_populates="driver")


class Circuit(Base):
    __tablename__ = "circuits"

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    country         = Column(String)
    city            = Column(String)
    lap_length_km   = Column(Float)
    total_turns     = Column(Integer)
    lap_record_time = Column(String)
    lap_record_year = Column(Integer)
    drs_zones       = Column(Integer)

    races = relationship("Race", back_populates="circuit")


class Season(Base):
    __tablename__ = "seasons"

    id   = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True, nullable=False)

    races = relationship("Race", back_populates="season")


class Race(Base):
    __tablename__ = "races"

    id         = Column(Integer, primary_key=True)
    season_id  = Column(Integer, ForeignKey("seasons.id"))
    circuit_id = Column(Integer, ForeignKey("circuits.id"))
    round      = Column(Integer)
    name       = Column(String)
    date       = Column(Date)
    has_sprint = Column(Boolean, default=False)

    season    = relationship("Season", back_populates="races")
    circuit   = relationship("Circuit", back_populates="races")
    results   = relationship("Result", back_populates="race")


class Result(Base):
    __tablename__ = "results"

    id              = Column(Integer, primary_key=True)
    race_id         = Column(Integer, ForeignKey("races.id"))
    driver_id       = Column(Integer, ForeignKey("drivers.id"))
    team_id         = Column(Integer, ForeignKey("teams.id"))
    grid_position   = Column(Integer)
    finish_position = Column(Integer)
    points          = Column(Float, default=0)
    status          = Column(String)
    fastest_lap     = Column(Boolean, default=False)

    race   = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    team   = relationship("Team", back_populates="results")