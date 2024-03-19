#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


class DBStorage:
    """Database storage class"""

    __engine = None
    __session = None
    __url_db = "mysql+mysqldb://{}:{}@{}/{}".format(
        os.getenv('HBNB_MYSQL_USER'),
        os.getenv('HBNB_MYSQL_PWD'),
        os.getenv('HBNB_MYSQL_HOST'),
        os.getenv('HBNB_MYSQL_DB')
    )
    __tables = ['User', 'City', 'State', 'Amenity', 'Place', 'Review']

    def __init__(self):
        """Constructor of DBStorage class"""
        self.__engine = create_engine(self.__url_db, pool_pre_ping=True)

        if os.getenv('HBNB_MYSQL_DB') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        obj_dict = {}
        if not cls:
            for table in self.__tables:
                rows = self.__session.query(eval(table)).all()
                for instance in rows:
                    key = instance.__class__.__name__ + '.' + instance.id
                    obj_dict.update({key: instance})
        else:
            if type(cls) == str:
                cls = eval(cls)
            rows = self.__session.query(cls).all()
            for instance in rows:
                key = instance.__class__.__name__ + '.' + instance.id
                obj_dict.update({key: instance})

        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
