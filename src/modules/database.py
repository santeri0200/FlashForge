# pylint: disable=redefined-builtin
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from tests import db_helper
from entities.reference import Reference, Article, Book, Inproceedings, Manual

def add_reference(ref):
    return ref.insert(db)

def edit_ref(ref):
    return ref.update(db)

def delete_reference(ref):
    return ref.delete(db)

def get_all_articles():
    return Reference.get_all(db, Article)

def get_all_books():
    return Reference.get_all(db, Book)

def get_all_inproceedings():
    return Reference.get_all(db, Inproceedings)

def get_all_manuals():
    return Reference.get_all(db, Manual)

def get_all_references():
    return [
        *get_all_articles(),
        *get_all_books(),
        *get_all_inproceedings(),
        *get_all_manuals(),
    ]

def article_from_id(id):
    return Reference.from_id(db, id, Article)

def book_from_id(id):
    return Reference.from_id(db, id, Book)

def inproceedings_from_id(id):
    return Reference.from_id(db, id, Inproceedings)

def manual_from_id(id):
    return Reference.from_id(db, id, Manual)

def ref_from_id(ref_type, id):
    match ref_type:
        case "article":
            return article_from_id(id)
        case "book":
            return book_from_id(id)
        case "inproceedings":
            return inproceedings_from_id(id)
        case "manual":
            return manual_from_id(id)

        case _:
            return None

def search_result(query):
    return [
        *Reference.get_like(db, query, Article),
        *Reference.get_like(db, query, Book),
        *Reference.get_like(db, query, Inproceedings),
        *Reference.get_like(db, query, Manual),
    ]

def reset_db():
    db_helper.reset_db()

def advanced_search_result(field, query):
    if field == "all_fields":
        return search_result(query)
    
    print(*Reference.get_by_field(db, "booktitle", "su", Inproceedings))

    return [
        *Reference.get_by_field(db, field, query, Article),
        *Reference.get_by_field(db, field, query, Book),
        *Reference.get_by_field(db, field, query, Inproceedings),
        *Reference.get_by_field(db, field, query, Manual),
    ]
