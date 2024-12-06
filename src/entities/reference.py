from abc import ABC, abstractmethod

class Reference(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def details(self):
        pass

class Article(Reference):
    def __init__(self, id=None, **kwargs):
        self.type     = "article"
        self.required = ["author", "title", "journal", "year"]
        self.special  = { "year": int, "volume": int, "number": int }
        self.fields   = { "id": id, "type": self.type, **kwargs }

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
        return {key: val if key in self.required else val or None for key, val in self.fields.items()}

class Book(Reference):
    def __init__(self, id=None, **kwargs):
        self.type     = "book"
        self.required = ["author", "title", "publisher", "year", "address"]
        self.special  = { "year": int }
        self.fields   = { "id": id, "type": self.type, **kwargs }

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
        return {key: val if key in self.required else val or None for key, val in self.fields.items()}

class Inproceedings(Reference):
    def __init__(self, id=None, **kwargs):
        self.type     = "inproceedings"
        self.required = ["author", "title", "booktitle", "year"]
        self.special  = { "year": int, "volume": int, "number": int }
        self.fields   = { "id": id, "type": self.type, **kwargs }

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
        return {key: val if key in self.required else val or None for key, val in self.fields.items()}