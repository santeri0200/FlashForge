# pylint: disable=redefined-builtin, use-a-generator, multiple-statements, consider-iterating-dictionary
from abc import ABC, abstractmethod
from sqlalchemy import text

class Reference(ABC):
    """Class for references"""
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def details(self):
        pass

    def validate(self):
        required_fields = all([
            required in self.fields.keys()
            for required in self.required
        ])

        def canbe(type, field):
            try:
                if field: type(field)
                return True
            except ValueError:
                return False

        typed_fields = all([
            canbe(self.special[field], self.fields[field])
            for field in self.fields
            if field in self.special.keys()
        ])

        return required_fields and typed_fields

    def details(self):
        default   = {key: None for key in self.required + self.optional}
        populated = {key: val or None for key, val in self.fields.items()}
        return {**default, **populated}

    def insert(self, db) -> bool:
        details = self.details()
        fields  = [key for key in details.keys()]
        sql = f"""
            INSERT INTO {self.table} ({", ".join(fields)}) VALUES ({", ".join([f":{key}" for key in fields])})
        """

        try:
            res = db.session.execute(text(sql), details)
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

class Article(Reference):
    """Class for article references"""
    def __init__(self, id=None, **kwargs):
        self.type     = "article"
        self.table    = "Articles"
        self.required = ["author", "title", "journal", "year"]
        self.optional = ["volume", "number", "pages", "month", "note"]
        self.special  = { "year": int, "volume": int, "number": int }
        self.fields   = { **kwargs }

class Book(Reference):
    """Class for book references"""
    def __init__(self, id=None, **kwargs):
        self.type     = "book"
        self.table    = "Books"
        self.required = ["author", "title", "publisher", "year", "address"]
        self.optional = []
        self.special  = { "year": int }
        self.fields   = { **kwargs }

class Inproceedings(Reference):
    """Class for inproceedings references"""
    def __init__(self, id=None, **kwargs):
        self.type     = "inproceedings"
        self.table    = "Inproceedings"
        self.required = ["author", "title", "booktitle", "year"]
        self.optional = ["editor", "volume", "number", "series", "pages",
                            "address", "month", "organization", "publisher"]
        self.special  = { "year": int, "volume": int, "number": int }
        self.fields   = { **kwargs }

class Manual(Reference):
    """Class for manuals references"""
    def __init__(self, id=None, **kwargs):
        self.type     = "manual"
        self.table    = "Manuals"
        self.required = ["title", "year"]
        self.optional = ["author", "organization", "address", "edition",
                            "month", "note"]
        self.special  = { "year": int }
        self.fields   = { **kwargs }    
