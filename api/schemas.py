from pydantic import BaseModel

class Team(BaseModel):
    team_id: str
    org_id: str
    city: str
    mascot: str
    start_year: int
    active: bool
    pfr_name: str

    class Config:
        orm_mode = True