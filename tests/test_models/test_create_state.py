import unittest
import MySQLdb

class TestConsoleMySQL(unittest.TestCase):
    def setUp(self):
        # Connect to the MySQL database
        self.conn = MySQLdb.connect(host='localhost', user='test_user', passwd='test_password', db='test_db')
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def test_create_state(self):
        # Get the initial number of records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Execute the console command to create a State object
        subprocess.run(['./console.py', 'create State name="California"'], text=True)

        # Get the updated number of records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        updated_count = self.cursor.fetchone()[0]

        # Assert that the difference in counts is +1
        self.assertEqual(updated_count - initial_count, 1)

if __name__ == '__main__':
    unittest.main()
