from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    date: str
    group: int

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: str
    date: str
    group: int
