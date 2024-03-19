#!/usr/bin/python3
""" Defines module DBStorage """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
import os
from models.base_model import Base


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
        """
        write query on the current database session
        to get all objects depending of the class
        """
        objs_list = []
        result_dict = {}
        if cls is None:
            for item in self.classes:
                objs_list.extend(self.__session.query(item).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs_list = self.__session.query(cls).all()
        for obj in objs_list:
            key = f"{obj.__class__.__name__}.{obj.id}"
            result_dict[key] = obj
        return result_dict

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
