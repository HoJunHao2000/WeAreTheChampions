from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db, init_db, Team
from database.models import TeamCreate, TeamUpdate
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Initialize the database (create tables if they don't exist)
    init_db()

@app.post("/teams", response_model=TeamCreate)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == team.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.get("/teams", response_model=List[TeamCreate])
def read_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@app.get("/teams/{name}", response_model=TeamCreate)
def read_team(name: str, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == name).first()
    return db_team

@app.put("/teams/{old_name}", response_model=TeamCreate)
def update_team(old_name: str, team: TeamUpdate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == old_name).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team.name = team.name
    db_team.date = team.date
    db_team.group = team.group
    db.commit()
    db.refresh(db_team)
    return db_team

@app.delete("/teams")
def delete_all_teams(db: Session = Depends(get_db)):
    db.query(Team).delete()
    db.commit()
    return {"message": "All teams deleted successfully"}
