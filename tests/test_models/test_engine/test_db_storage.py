#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
from datetime import datetime
import inspect
from models.amenity import Amenity
from models.base_model import BaseModel
import models
from models.engine import db_storage
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place
import pycodestyle
import unittest
import json
import os

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
storageer = os.getenv("HBNB_TYPE_STORAGE")


class TestFileStorage(unittest.TestCase):
    """Fs is working"""

    @unittest.skipIf(storageer != 'db', "not the db")
    def test_save(self):
        """Tsaving to ghe json file """

    @unittest.skipIf(storageer != 'db', "not the db")
    def test_new(self):
        """new obj"""

    @unittest.skipIf(storageer != 'db', "not the db")
    def test_all_returns_dict(self):
        """is it dict"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(storageer != 'db', "not the db")
    def test_no_classes(self):
        """is it wies no class ?"""
