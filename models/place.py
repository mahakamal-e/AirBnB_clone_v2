#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
import os
from models.review import Review
import models
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place ito stay """
    __tablename__ = 'places'
    city_id = Column('city_id', String(60), ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column('user_id', String(60), ForeignKey('users.id'),
                     nullable=False)
    name = Column('name', String(128), nullable=False)
    description = Column('description', String(1024))
    number_rooms = Column('number_rooms', Integer, default=0, nullable=False)
    number_bathrooms = Column('number_bathrooms', Integer, default=0,
                              nullable=False)
    max_guest = Column('max_guest', Integer, default=0, nullable=False)
    price_by_night = Column('price_by_night', Integer, default=0,
                            nullable=False)
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', cascade='all, delete')
    else:
        @property
        def reviews(self):
            reviews_list = []

            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    reviews_list.append(review)

            return reviews_list
