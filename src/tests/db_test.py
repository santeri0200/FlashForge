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
        ref1 = Book(
            author    = 'Author',
            year      = 2024,
            title     = 'Title',
            publisher = 'Publisher',
            address   = 'Address',
        )
        ref2 = Inproceedings(
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
        ref3 = Manual(
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
            self.assertTrue(ref1.insert(db))
            self.assertTrue(ref2.insert(db))
            self.assertTrue(ref3.insert(db))
            res = database.get_all_articles()
            ref.id = res[0].id
            self.assertEqual([val.details() for val in res], [ref.details()])
            res = database.get_all_books()
            ref1.id = res[0].id
            self.assertEqual([val.details() for val in res], [ref1.details()])
            res = database.get_all_inproceedings()
            ref2.id = res[0].id
            self.assertEqual([val.details() for val in res], [ref2.details()])
            res = database.get_all_manuals()
            ref3.id = res[0].id
            self.assertEqual([val.details() for val in res], [ref3.details()])

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
            self.assertEqual([val.details() for val in res], [expected])

            res = database.search_result('thor')
            self.assertEqual([val.details() for val in res], [expected])

            res = database.search_result('2024')
            self.assertEqual([val.details() for val in res], [expected])

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
            res = database.ref_from_id("article", expected.id)
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

    def test_advanced_search(self):
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
            self.assertTrue(database.add_reference(ref))
            res = database.advanced_search_result('author', 'au')
            self.assertEqual([val.details() for val in res], [ref.details()])
            res = database.advanced_search_result('title', 'tle')
            self.assertEqual([val.details() for val in res], [ref.details()])
            res = database.advanced_search_result('journal', 'rnal')
            self.assertEqual([val.details() for val in res], [ref.details()])
            res = database.advanced_search_result('year', '1999')
            self.assertEqual([val.details() for val in res], [])
            res = database.advanced_search_result('all_fields', 'au')
            self.assertEqual([val.details() for val in res], [ref.details()])

    def test_order_references_by_year(self):
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
        ref2 = Article(
            author  = 'Author2',
            title   = 'Title2',
            journal = 'Journal2',
            year    = 2022,
            volume  = None,
            number  = None,
            pages   = None,
            month   = None,
            note    = None,
        )

        with self.context:
            self.assertTrue(database.add_reference(ref))
            self.assertTrue(database.add_reference(ref2))
            res = database.order_references('old_to_new')
            self.assertEqual(res[0].details().get("author"), 'Author2')
            res = database.order_references('new_to_old')
            self.assertEqual(res[0].details().get("author"), 'Author')
