import unittest
from mock import patch
from DatabaseHandler import DatabaseHandler
import os


class TestDatabaseHandler(unittest.TestCase):

    def tearDown(self):
        if os.path.exists('unit_test_db.sqlite3'):
            os.remove('unit_test_db.sqlite3')
        if os.path.exists('test_file.csv'):
            os.remove('test_file.csv')

    # constructor tests
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_connects(self,
                                          mock_sql):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_sql.connect.assert_called_once_with('unit_test_db.sqlite3')

    @patch('DatabaseHandler.sql')
    def test_handler_constructor_default_db_file_name_is_correct(self,
                                                                 mock_sql):
        handler = DatabaseHandler()
        mock_sql.connect.assert_called_once_with('db.sqlite3')

    def test_handler_constructor_creates_Source_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        c = handler.conn.cursor()
        c.execute("select name from sqlite_master where "
                  "type='table' and name='Source'")
        self.assertTrue(c.fetchone(), "Source table not created in constructor")

    def test_handler_constructor_creates_Source_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        c = handler.conn.cursor()
        c.execute("select name from sqlite_master where "
                  "type='table' and name='TransitStop'")
        self.assertTrue(c.fetchone(),
                        "TransitStop table not created in constructor")

    # _create_location_table tests
    def test_handler_create_location_creates_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._create_location_table_if_not_exists('test_table')
        c = handler.conn.cursor()
        c.execute("select name from sqlite_master where "
                  "type='table' and name='test_table'")
        self.assertTrue(c.fetchone(), "test_table not created")

    # add_rows_from_csv tests
    def test_handler_load_file_into_table_inserts_one_record(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        with open('test_file.csv', 'w') as f:
            f.write('latitude,longitude\n')
            f.write('8,12\n')
        handler.add_rows_from_csv('test_file.csv', 'Source')
        c = handler.conn.cursor()
        c.execute("select * from Source")
        row = c.fetchone()
        self.assertEqual(8, row[0])
        self.assertEqual(12, row[1])
