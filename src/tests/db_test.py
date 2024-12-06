import unittest
from tests import db_helper
from modules import database
from config import app

from entities.reference import Article

class TestDatabase(unittest.TestCase):
    """Class for testing the database"""

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
            db_helper.reset_db()

    def test_database_add(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))

    def test_database_query(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))
            res = database.get_all_articles()
            ref.fields["id"] = res[0].fields["id"]
            self.assertEqual([val.details() for val in res], [ref.details()])

    def test_database_add_duplicate(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))
            self.assertFalse(database.add_article(ref))

    def test_database_valid_search(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))
            (res, _, _) = database.search_result('Au')

            expected = ref.details()
            expected["id"] = res[0].id
            self.assertEqual([Article(**val._asdict()).details() for val in res], [expected])

            (res, _, _) = database.search_result('thor')
            expected["id"] = res[0].id
            self.assertEqual([Article(**val._asdict()).details() for val in res], [expected])

            (res, _, _) = database.search_result('2024')
            expected["id"] = res[0].id
            self.assertEqual([Article(**val._asdict()).details() for val in res], [expected])

    def test_database_invalid_search(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))

            (res, _, _) = database.search_result('Invalid')
            self.assertEqual(res, [])

            (res, _, _) = database.search_result('1999')
            self.assertEqual(res, [])

    def test_database_edit_article(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))
            res = database.get_all_articles()

            expected = Article(
                id      = res[0].fields["id"],
                author  = 'Author',
                title   = 'Title',
                journal = 'Journal',
                year    = 2024,
                volume  = None,
                number  = None,
                pages   = None,
                month   = None,
                note    = None,
            )

            self.assertTrue(database.edit_article(expected))
            res = database.article_from_id(expected.fields["id"])
            self.assertEqual(res.details(), expected.details())

    def test_database_delete_article(self):
        ref = Article(
            author  = 'Author',
            title   = 'Title',
            journal = 'Journal',
            year    = 2024,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_article(ref))
            res = database.get_all_articles()
            self.assertTrue(database.delete_reference("article", res[0].fields["id"]))
            res = database.get_all_articles()
            self.assertEqual(res, [])
