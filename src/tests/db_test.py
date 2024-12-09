import unittest
from tests import db_helper
from modules import database
from config import app, db

from entities.reference import Article, Book, Inproceedings, Manual

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

    def test_database_add_article(self):
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
            self.assertTrue(ref.insert(db))

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
            self.assertTrue(ref.insert(db))
            res = database.get_all_articles()
            ref.fields["id"] = res[0].id
            res[0].fields["id"] = res[0].id
            self.assertEqual([val.details() for val in res], [ref.details()])

    def test_database_add_duplicate_article(self):
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
            self.assertTrue(ref.insert(db))
            self.assertFalse(ref.insert(db))

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
            self.assertTrue(ref.insert(db))
            res = database.search_result('Au')

            expected = ref.details()
            self.assertEqual([res[0].details()], [expected])

            res = database.search_result('thor')
            self.assertEqual([res[0].details()], [expected])

            res = database.search_result('2024')
            self.assertEqual([res[0].details()], [expected])

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
            self.assertTrue(ref.insert(db))

            res = database.search_result('Invalid')
            self.assertEqual(res, [])

            res = database.search_result('1999')
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
            self.assertTrue(ref.insert(db))
            res = database.get_all_articles()

            expected = Article(
                id      = res[0].id,
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

            self.assertTrue(database.edit_ref(expected))
            res = database.article_from_id(res[0].id)
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
            self.assertTrue(ref.insert(db))
            res = database.get_all_articles()
            self.assertTrue(database.delete_reference(res[0]))
            res = database.get_all_articles()
            self.assertEqual(res, [])

    def test_database_add_book(self):
        ref = Book(
            author    = 'Author',
            year      = 2024,
            title     = 'Title',
            publisher = 'Publisher',
            address   = 'Address',
    )

        with self.context:
            self.assertTrue(ref.insert(db))

    def test_database_add_duplicate_book(self):
        ref = Book(
            author    = 'Author',
            year      = 2024,
            title     = 'Title',
            publisher = 'Publisher',
            address   = 'Address',
    )

        with self.context:
            self.assertTrue(ref.insert(db))
            self.assertFalse(ref.insert(db))

    def test_database_add_inproceedings(self):
        ref = Inproceedings(
            author       = 'Author',
            title        = 'Title',
            booktitle    = 'Booktitle',
            year         = 2024,
            editor       = None,
            volume       = None,
            number       = None,
            series       = None,
            pages        = None,
            address      = None,
            organization = None,
            month        = None,
            publisher    = None,
        )

        with self.context:
            self.assertTrue(ref.insert(db))

    def test_database_add_duplicate_inproceedings(self):
        ref = Inproceedings(
            author       = 'Author',
            title        = 'Title',
            booktitle    = 'Booktitle',
            year         = 2024,
            editor       = None,
            volume       = None,
            number       = None,
            series       = None,
            pages        = None,
            address      = None,
            organization = None,
            month        = None,
            publisher    = None,
        )

        with self.context:
            self.assertTrue(ref.insert(db))
            self.assertFalse(ref.insert(db))

    def test_database_add_manual(self):
        ref = Manual(
            title        = 'Title',
            year         = 2024,
            author       = None,
            organization = None,
            address      = None,
            edition      = None,
            month        = None,
            note         = None,
        )

        with self.context:
            self.assertTrue(ref.insert(db))

    def test_database_add_duplicate_manual(self):
        ref = Manual(
            title        = 'Title',
            year         = 2024,
            author       = None,
            organization = None,
            address      = None,
            edition      = None,
            month        = None,
            note         = None,
        )

        with self.context:
            self.assertTrue(ref.insert(db))
            self.assertFalse(ref.insert(db))
