from datetime import datetime

from pydantic import BaseModel

class LogEntry(BaseModel):
    message: str
    timestamp: datetime