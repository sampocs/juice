from sqlalchemy import Column, Integer, Text, Boolean
from core.database import Base


class Team(Base):

    __tablename__ = 'teams'

    team_id    = Column('team_id', Text, primary_key=True, index=True)
    org_id     = Column(Text, index=True, nullable=False)
    city       = Column(Text, nullable=False)
    mascot     = Column(Text, nullable=False)
    start_year = Column(Integer, nullable=False)
    active     = Column(Boolean, nullable=False)
    pfr_name   = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Team: {self.city} {self.mascot} ({self.team_id})>'
