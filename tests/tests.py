import unittest
import sys

sys.path.insert(1, 'C:\\Users\\maksi\\OneDrive\\Рабочий стол\\СибГУТИ\\4 курс\\8 Семестр\\diplom\\server')

from model.src.database_handler import Database_handler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db_handler = Database_handler()

    def test_Inizialization(self):
        res = self.db_handler.execute("SELECT 1, 2, 3")
        self.assertEqual(res.first(), (1, 2, 3))
        
if __name__ == "__main__":
    unittest.main()