"""Module Entity Player"""
from datetime import datetime
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from .base import Base


class Player(Base):
    """Entity Player"""
    __tablename__ = 'PLAYER'
    id:Mapped[int]= mapped_column(Integer,autoincrement=True, primary_key=True,unique=True,nullable=False,name='ID',)
    weight:Mapped[int]= mapped_column(Integer, name='WEIGHT')
    hight:Mapped[int]= mapped_column(Integer, name='HIGHT')
    dorsal_number:Mapped[str]= mapped_column(String(255), name='DORSAL_NUMBER')
    position:Mapped[str]= mapped_column(String(255), name='POSITION')
    skil_ful_foot:Mapped[str]= mapped_column(String(255), name='SKIL_FUL_FOOT')
    is_full_profile:Mapped[bool]= mapped_column(Integer, name='IS_FULL_PROFILE')
    goals:Mapped[int]= mapped_column(Integer, name='GOALS')
    assists:Mapped[int]= mapped_column(Integer, name='ASSISTS')
    goals_againts:Mapped[int]= mapped_column(Integer, name='GOALS_AGAINTS')
    red_cards:Mapped[int]= mapped_column(Integer, name='RED_CARDS')
    yellow_cards:Mapped[int]= mapped_column(Integer, name='YELLOW_CARDS')
    games_played:Mapped[int]= mapped_column(Integer, name='GAMES_PLAYED')
    titles:Mapped[int]= mapped_column(Integer, name='TITLES')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name='CREATED_AT')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, name='UPDATED_AT')