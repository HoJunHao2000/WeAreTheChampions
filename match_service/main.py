from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db, init_db, Match
from database.models import MatchCreate, MatchUpdate, MatchResponse
from typing import List

app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Initialize the database (create tables if they don't exist)
    init_db()

@app.post("/matches", response_model=MatchCreate)
def add_match(match: MatchCreate, db: Session = Depends(get_db)):
    db_match = db .query(Match).filter(Match.team_a == match.team_a, Match.team_b == match.team_b).first()
    if db_match:
        raise HTTPException(status_code=400, detail="Match already exists")
    db_match = Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

@app.get("/matches/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    return db_match

@app.get("/matches", response_model=List[MatchResponse])
def all_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()

@app.put("/matches/{match_id}", response_model=MatchCreate)
def edit_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    db_match.team_a = match.team_a
    db_match.team_b = match.team_b
    db_match.goals_a = match.goals_a
    db_match.goals_b = match.goals_b
    db.commit()
    db.refresh(db_match)
    return db_match

@app.delete("/matches")
def delete_all_matches(db: Session = Depends(get_db)):
    db.query(Match).delete()
    db.commit()
    return {"message": "All matches deleted successfully"}