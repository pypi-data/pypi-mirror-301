from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Country(Base):
    __tablename__ = 'COUNTRY'
    id:Mapped[int]= mapped_column(Integer,autoincrement=True, primary_key=True,unique=True,nullable=False,name='ID',)
    name:Mapped[str]= mapped_column(String(255), name='NAME')
    code:Mapped[str]= mapped_column(String(255), name='CODE')
