#!/usr/bin/python3
""" Unittests for database """
import unittest
import MySQLdb


class TestStateCreation(unittest.TestCase):
    def setUp(self):
        self.db = MySQLdb.connect(host="localhost", user="hbnb_test",
                                  passwd="hbnb_test_pwd", db="hbnb_test_db")
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT COUNT(*) FROM states")
        self.initial_state_count = self.cursor.fetchone()[0]

    def tearDown(self):
        self.db.close()

    def test_create_state(self):
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_state_count = self.cursor.fetchone()[0]

        self.assertEqual(final_state_count, self.initial_state_count + 1,
                         "State creation test failed")

if __name__ == '__main__':
    unittest.main()
