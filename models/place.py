#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
import os
from models.review import Review
import models
from sqlalchemy.orm import relationship


place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
               primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
               primary_key=True, nullable=False)
        )


class Place(BaseModel, Base):
    """ A place ito stay """
    __tablename__ = 'places'
    #city_id = Column('city_id', String(60), ForeignKey('cities.id'),
     #                nullable=False)
    user_id = Column('user_id', String(60),
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
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:

        @property
        def reviews(self):
            """ Get list of reviews related to place """
            reviews_list = []

            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    reviews_list.append(review)

            return reviews_list

        @property
        def amenities(self):
            """Get list of Amenities """
            amenity_list = []

            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)

            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """setter values of attribute Amenities"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
