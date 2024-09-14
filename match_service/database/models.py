from pydantic import BaseModel

class MatchBase(BaseModel):
    team_a: str
    team_b: str
    goals_a: int
    goals_b: int

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    team_a: str
    team_b: str
    goals_a: int
    goals_b: int

class MatchResponse(MatchBase):
    id: int

    class Config:
        orm_mode = True