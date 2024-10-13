"""Module for User entity"""
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    """Entity User"""
    __tablename__ = 'USER'
    uuid:Mapped[str]= mapped_column(String(255), primary_key=True,unique=True,nullable=False,name='UUID',)
    full_name:Mapped[str]= mapped_column(String(255), nullable=False, name='FULL_NAME')
    gender:Mapped[str]= mapped_column(String(255), name='GENDER')
    birthdate:Mapped[datetime]= mapped_column(DateTime, name='BIRTHDATE')
    email:Mapped[str]= mapped_column(String(255), name='EMAIL', unique=True, nullable=False)
    cellphone:Mapped[str]= mapped_column(String(255), name='CELLPHONE', nullable=False)
    create_date:Mapped[datetime]= mapped_column(DateTime, name='CREATE_DATE', default=datetime.now)
    last_update_date:Mapped[datetime]= mapped_column(DateTime, name='LAST_UPDATE_DATE', default=datetime.now, onupdate=datetime.now)
    nick_name:Mapped[str]= mapped_column(String(255), name='NICK_NAME', unique=True,nullable=False)
    device_id:Mapped[str]= mapped_column(String(255), name='DEVICE_ID')
    player_id:Mapped[int]= mapped_column(Integer, ForeignKey('PLAYER.ID'), nullable=True,name='PLAYER_ID')
    city_id:Mapped[int]= mapped_column(Integer, ForeignKey('CITY.ID'), name='CITY_ID')