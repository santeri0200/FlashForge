import unittest
import tests.db_helper as db_helper
import modules.database as database
from config import app, db

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.context = cls.app.app_context()

        with cls.context:
          db_helper.setup_db()

    def setUp(self):
        pass

    def tearDown(self):
        with self.context:
            db_helper.reset_db("articles")
    
    def test_database_add(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))

    def test_database_query(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            res = database.get_all_articles()
            expected = [(res[0].id, 'Author', 'Title', 'Journal', 2024)]
            self.assertEqual(res, expected)
    
    def test_database_add_duplicate(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            self.assertFalse(database.add_article('Author', 'Title', 'Journal', 2024))
