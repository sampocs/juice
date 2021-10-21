from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from core.database import Base
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

class Team(Base):

    __tablename__ = 'teams'

    team_id    = Column('team_id',    Text, primary_key=True)
    org_id     = Column('org_id',     Text)
    city       = Column('city',       Text)
    mascot     = Column('mascot',     Text)
    start_year = Column('start_year', Integer)
    active     = Column('active',     Boolean)
    pfr_id     = Column('pfr_id',     Text)
    games      = relationship('Game', back_populates='home_team')

    def __repr__(self) -> str:
        return f'<Team: {self.city} {self.mascot} ({self.team_id})>'


class Game(Base):

    __tablename__ = 'games'

    game_id      = Column('game_id',      Text, primary_key=True)
    season       = Column('season',       Integer)
    week         = Column('week',         Integer)
    datetime     = Column('datetime',     DateTime)
    home_team_id = Column('home_team_id', Text, ForeignKey('teams.team_id'))
    home_team    = relationship('Team',   back_populates='games')
    away_team_id = Column('away_team_id', Text)
    home_score   = Column('home_score',   Integer, nullable=True)
    away_score   = Column('away_score',   Integer, nullable=True)
    has_pbp      = Column('has_pbp',      Boolean, default=False)
    prf_game_id  = Column('prf_game_id',  Text,    nullable=True)

    def __repr__(self) -> str:
        return f'<Game: {self.game_id} | {self.away_team_id} @ {self.home_team_id}>'
