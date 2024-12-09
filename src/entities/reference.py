# pylint: disable=redefined-builtin, use-a-generator, multiple-statements, consider-iterating-dictionary
from abc import ABC, abstractmethod
from sqlalchemy import text

class Reference(ABC):
    """Class for references"""
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

    def from_id(db, id, cls):
        sql = f"""
            SELECT * FROM {cls.table} WHERE id = :id
        """

        print(id, sql)

        try:
            res = db.session.execute(text(sql), { "id": id })
        except:
            return cls()

        row = res.fetchone()
        return cls(**row._asdict()) if row else cls()
        

    def get_all(db, cls):
        sql = f"""
            SELECT * FROM {cls.table}
        """

        try:
            res = db.session.execute(text(sql))
        except:
            return []

        return [cls(**row._asdict()) for row in res.fetchall()]

    def insert(self, db) -> bool:
        details = self.details()
        fields  = [key for key in details.keys()]
        sql = f"""
            INSERT INTO {self.table} ({", ".join(fields)}) VALUES ({", ".join([f":{key}" for key in fields])})
        """

        print(sql, details)

        try:
            res = db.session.execute(text(sql), details)
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

class Article(Reference):
    """Class for article references"""
    type     = "article"
    table    = "Articles"
    required = ["author", "title", "journal", "year"]
    optional = ["volume", "number", "pages", "month", "note"]
    special  = { "year": int, "volume": int, "number": int }

    def __init__(self, id=None, **kwargs):
        self.id     = id
        self.fields = { **kwargs }    

class Book(Reference):
    """Class for book references"""
    type     = "book"
    table    = "Books"
    required = ["author", "title", "publisher", "year", "address"]
    optional = []
    special  = { "year": int }

    def __init__(self, id=None, **kwargs):
        self.id     = id
        self.fields = { **kwargs }    

class Inproceedings(Reference):
    """Class for inproceedings references"""
    type     = "inproceedings"
    table    = "Inproceedings"
    required = ["author", "title", "booktitle", "year"]
    optional = ["editor", "volume", "number", "series", "pages", "address",
                "month", "organization", "publisher"]
    special  = { "year": int, "volume": int, "number": int }

    def __init__(self, id=None, **kwargs):
        self.id     = id
        self.fields = { **kwargs }    

class Manual(Reference):
    """Class for manuals references"""
    type     = "manual"
    table    = "Manuals"
    required = ["title", "year"]
    optional = ["author", "organization", "address", "edition", "month", "note"]
    special  = { "year": int }

    def __init__(self, id=None, **kwargs):
        self.id     = id
        self.fields = { **kwargs }    
