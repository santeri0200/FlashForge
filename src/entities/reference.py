class Field:
    def __init__(self, value, required):
        self.value = value
        self.required = required

class Article:
    def __init__(self, id, author, title, journal, year, volume=None, number=None, pages=None, month=None, note=None):
        self.type = "article"
        self.id = id
        self.author = Field(author, True)
        self.title = Field(title, True)
        self.journal = Field(journal, False)
        self.year = Field(year, True)
        self.volume = Field(volume, False)
        self.number = Field(number, False)
        self.pages = Field(pages, False)
        self.month = Field(month, False)
        self.note = Field(note, False)

    def details(self):
        return {
            "id": self.id,
            "type": "article",
            "author": self.author.value,
            "title": self.title.value,
            "journal": self.journal.value,
            "year": self.year.value,
            "volume": self.volume.value,
            "number": self.number.value,
            "pages": self.pages.value,
            "month": self.month.value,
            "note": self.note.value
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

