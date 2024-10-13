from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship,mapped_column
from .base import Base
from .country import Country


class Department(Base):
    __tablename__ = 'DEPARTMENT'
    id:Mapped[int]= mapped_column(Integer,autoincrement=True, primary_key=True,unique=True,nullable=False,name='ID',)
    name:Mapped[str]= mapped_column(String(255), name='NAME')
    code:Mapped[str]= mapped_column(String(255), name='CODE')
    country_id:Mapped[int]= mapped_column(Integer, ForeignKey('COUNTRY.ID'), name='COUNTRY_ID')

    #country:Mapped[Country]= relationship('Country', back_populates='DEPARTMENT')
