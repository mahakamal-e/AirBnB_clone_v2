#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    __table_args__ = (
        {'mysql_default_charset': 'latin1'})

    name = Column('name', String(128), nullable=False)
    state_id = Column('state_id', String(60), ForeignKey('states.id'),
                      nullable=False)
