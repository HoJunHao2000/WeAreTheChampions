from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db, init_db, Log
from database.models import LogEntry
from typing import List

app = FastAPI()


@app.on_event("startup")
def on_startup():
    # Initialize the database (create tables if they don't exist)
    init_db()

@app.post("/logs")
def create_log(log: LogEntry, db: Session = Depends(get_db)):
    db_log = Log(message=log.message, timestamp=log.timestamp)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"status": "success"}

@app.get("/logs", response_model=List[LogEntry])
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).order_by(Log.timestamp.desc()).all()
    return [{"message": log.message, "timestamp": log.timestamp} for log in logs]