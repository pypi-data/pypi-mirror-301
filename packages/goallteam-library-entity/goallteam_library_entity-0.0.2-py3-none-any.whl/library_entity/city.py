from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship,mapped_column
from .base import Base


class City(Base):
    __tablename__ = 'CITY'
    id:Mapped[int]= mapped_column(Integer,autoincrement=True, primary_key=True,unique=True,nullable=False,name='ID',)
    name:Mapped[str]= mapped_column(String(255), name='NAME')
    code:Mapped[str]= mapped_column(String(255), name='CODE')
    department_id:Mapped[int]= mapped_column(Integer, ForeignKey('DEPARTMENT.ID'), name='DEPARTMENT_ID')
