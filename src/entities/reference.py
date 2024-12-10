# pylint: disable=bare-except, redefined-builtin, use-a-generator, multiple-statements, consider-iterating-dictionary
from sqlalchemy import text

class Reference:
    """Class for references"""
    type     = "generic_reference"
    table    = ""
    required = []
    optional = []
    special  = {}
    id       = None
    fields   = {}

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
            canbe(self.special[key], val)
            for key, val in self.fields.items()
            if key in self.special.keys()
        ])

        return required_fields and typed_fields

    def details(self):
        default   = {key: None for key in self.required + self.optional}
        populated = {key: val or None for key, val in self.fields.items()}
        return {**default, **populated}

    # pylint: disable=no-self-argument
    def from_id(db, id, cls):
        sql = f"""
            SELECT * FROM {cls.table} WHERE id = :id
        """

        print(id, sql)

        try:
            # pylint: disable=no-member
            res = db.session.execute(text(sql), { "id": id })
        except:
            return cls()

        row = res.fetchone()
        return cls(**row._asdict()) if row else cls()

    # pylint: disable=no-self-argument
    def get_all(db, cls):
        sql = f"""
            SELECT * FROM {cls.table}
        """

        try:
            # pylint: disable=no-member
            res = db.session.execute(text(sql))
        except:
            return []

        return [cls(**row._asdict()) for row in res.fetchall()]

    # pylint: disable=no-self-argument
    def get_like(db, query, cls):
        fields = [f"CAST({key} AS TEXT) ILIKE :query" for key in cls.required + cls.optional]
        sql = f"""
            SELECT *
            FROM {cls.table}
            WHERE {" OR ".join(fields)}
        """

        try:
            # pylint: disable=no-member
            res = db.session.execute(text(sql), {"query": f"%{query}%"})
            return [cls(**row._asdict()) for row in res.fetchall()]
        except:
            # pylint: disable=no-member
            db.session.rollback()
            return []


    # pylint: disable=no-self-argument
    def get_by_field(db, field, query, cls):
        sql = f"""
            SELECT *
            FROM {cls.table}
            WHERE CAST({field} AS TEXT) ILIKE :query
        """

        try:
            # pylint: disable=no-member
            res = db.session.execute(text(sql), {"query": f"%{query}%"})
            return [cls(**row._asdict()) for row in res.fetchall()]
        except:
            # pylint: disable=no-member
            db.session.rollback()
            return []

    def insert(self, db) -> bool:
        details = self.details()
        fields  = details.keys()
        sql = f"""
            INSERT INTO {self.table} ({", ".join(fields)}) VALUES ({", ".join([f":{key}" for key in fields])})
        """

        print(sql, details)

        try:
            db.session.execute(text(sql), details)
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def update(self, db) -> bool:
        details = self.details()
        sql = f"""
            UPDATE {self.table}
            SET {", ".join([f"{key}=:{key}" for key in details.keys()])}
            WHERE id = :id
        """

        try:
            db.session.execute(text(sql), {"id": self.id, **details})
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def delete(self, db) -> bool:
        sql = f"""
            DELETE FROM {self.table} where id=:id
        """

        try:
            db.session.execute(text(sql), {"id": self.id})
        except:
            db.session.rollback()
            return False

        db.session.commit()
        return True

    def generate(self):
        header = f"{self.type}-{self.id}"
        fields = "\n".join([f"\t{key} = {{{val}}}," for key, val in self.fields.items() if val])
        return f"@{self.type}{{{header},\n{fields}\n}}\n"

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
