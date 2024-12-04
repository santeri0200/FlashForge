class Article:
    def __init__(self, id, author, title, journal, year, volume=None, number=None, pages=None, month=None, note=None):
        self.type = "article"
        self.id = id
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.number = number
        self.pages = pages
        self.month = month
        self.note = note

    def details(self):
        return {
            "id": self.id,
            "type": "article",
            "author": self.author,
            "title": self.title,
            "journal": self.journal,
            "year": self.year,
            "volume": self.volume,
            "number": self.number,
            "pages": self.pages,
            "month": self.month,
            "note": self.note
        }

class Book:
    def __init__(self, id, author, year, title, publisher, address):
        self.id = id
        self.year = year
        self.author = author
        self.title = title
        self.publisher = publisher
        self.address = address

    def details(self):
        return {
            "type": "book",
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "year": self.year,
            "publisher": self.publisher,
            "address": self.address
        }

