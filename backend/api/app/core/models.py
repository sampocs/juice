from sqlalchemy import Column, Integer, Text, Boolean, DateTime
from core.database import Base


class Team(Base):

    __tablename__ = 'teams'

    team_id    = Column('team_id',    Text, primary_key=True)
    org_id     = Column('org_id',     Text)
    city       = Column('city',       Text)
    mascot     = Column('mascot',     Text)
    start_year = Column('start_year', Integer)
    active     = Column('active',     Boolean)
    pfr_name   = Column('pft_name',   Text)

    def __repr__(self) -> str:
        return f'<Team: {self.city} {self.mascot} ({self.team_id})>'


class Game(Base):

    __tablename__ = 'games'

    game_id      = Column('game_id',      Text, primary_key=True)
    season       = Column('season',       Integer)
    week         = Column('week',         Integer)
    datetime     = Column('datetime',     DateTime)
    home_team_id = Column('home_team_id', Text)
    away_team_id = Column('away_team_id', Text)
    home_score   = Column('home_score',   Integer)
    away_score   = Column('away_score',   Integer)
    has_pbp      = Column('has_pbp',      Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Game: {self.game_id} | {self.away_team_id} @ {self.home_team_id}>'
