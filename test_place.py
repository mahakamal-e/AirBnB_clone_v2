#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Place(BaseModel, Base):
    __tablename__ = 'place'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
dummy_city_id = "some_city_id"
dummy_user_id = "some_user_id"

try:
  new_place = Place(city_id=dummy_city_id, user_id=dummy_user_id, name="Test Place")
  print("Place created successfully!")
except Exception as e:
  print("Error creating Place:", e)

