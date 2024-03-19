#!/usr/bin/python3
""" Defines module DBStorage """
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
    """
    manages the connection to the database, session management
    and operations related to querying, adding, saving
    and deleting objects.
    """
    __engine = None
    __session = None
    classes_names = [User, State, City, Amenity, Place, Review]

    __db_connection = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')
    )
                                               
    def __init__(self):
        """ initalization instance from class DBStorage """
        self.__engine = create_engine(self.__db_connection,
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        objs = []
        dct = {}
        if cls is None:
            for item in self.classes:
                objs.extend(self.__session.query(item).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            objs = self.__session.query(cls).all()

        for obj in objs:
            dct[obj.__class__.__name__ + '.' + obj.id] = obj
        return dct

    def new(self, obj):
        """ Method to add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables in the database
        'reload data from database'
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ close connection with database server"""
        self.__session.close()
