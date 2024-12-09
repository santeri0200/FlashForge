# pylint: disable=redefined-builtin, bare-except
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from sqlalchemy import text
from tests import db_helper
from entities.reference import Reference, Article, Book, Inproceedings, Manual

def add_reference(ref):
    return ref.insert(db)

def edit_article(ref):
    try:
        sql = text("""
            UPDATE articles
            SET author=:author,
                title=:title,
                journal=:journal,
                year=:year,
                volume=:volume,
                number=:number,
                pages=:pages,
                month=:month,
                note=:note
            WHERE id=:id
        """)
        db.session.execute(sql, ref.details())
    except:
        return False
    db.session.commit()
    return True

def edit_ref(ref_type, id, details):
    table_names = {
        "article": "articles",
        "book": "books",
        "inproceedings": "inproceedings"
    }
    updated_fields = ""
    for key in details:
        updated_fields += key + "=:" + key
        if key != list(details.keys())[-1]:
            updated_fields += ", "

    try:
        sql = text(f"UPDATE {table_names[ref_type]} SET {updated_fields} WHERE id={id}")
        db.session.execute(sql, details)
    except:
        return False
    db.session.commit()
    return True

def delete_reference(ref_type, id):
    table_names = {
        "article": "Articles",
        "book": "Books",
        "inproceedings": "inproceedings"
    }
    try:
        sql = text(f"DELETE FROM {table_names[ref_type]} WHERE id=:id")
        db.session.execute(sql, {"id":id})
    except:
        return False
    db.session.commit()
    return True

def get_all_references():
    return [
        *get_all_articles(),
        *get_all_books(),
        *get_all_inproceedings(),
        *get_all_manuals(),
    ]

def get_all_articles():
    return Reference.get_all(db, Article)

def get_all_books():
    return Reference.get_all(db, Book)

def get_all_inproceedings():
    return Reference.get_all(db, Inproceedings)

def get_all_manuals():
    return Reference.get_all(db, Manual)

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
    if query is None:
        return []

    res = db.session.execute(
        text("""
            SELECT *
            FROM articles
            WHERE
                LOWER(author) LIKE LOWER(:query)
                OR LOWER(title) LIKE LOWER(:query)
                OR LOWER(journal) LIKE LOWER(:query)
                OR CAST(year AS TEXT) LIKE :query
                OR CAST(volume AS TEXT) LIKE :query
                OR CAST(number AS TEXT) LIKE :query
                OR LOWER(pages) LIKE LOWER(:query)
                OR LOWER(month) LIKE LOWER(:query)
                OR LOWER(note) LIKE LOWER(:query)
            ORDER BY id DESC
        """),
        {"query": f"%{query.lower()}%"}
    )

    articles = [Article(**row._asdict()) for row in res.fetchall()]

    res = db.session.execute(
        text("""
            SELECT *
            FROM books
            WHERE
                LOWER(author) LIKE LOWER(:query)
                OR LOWER(title) LIKE LOWER(:query)
                OR LOWER(publisher) LIKE LOWER(:query)
                OR LOWER(address) LIKE LOWER(:query)
                OR CAST(year as TEXT) LIKE :query
             ORDER BY id DESC
         """),
         { "query": f"%{query.lower()}%" }
    )

    books = [Book(**row._asdict()) for row in res.fetchall()]

    res = db.session.execute(
        text("""
            SELECT *
            FROM inproceedings
            WHERE
                LOWER(author) LIKE LOWER(:query)
                OR LOWER(title) LIKE LOWER(:query)
                OR LOWER(booktitle) LIKE LOWER(:query)
                OR CAST(year AS TEXT) LIKE :query
                OR CAST(volume AS TEXT) LIKE :query
                OR CAST(number AS TEXT) LIKE :query
                OR LOWER(series) LIKE LOWER(:query)   
                OR LOWER(pages) LIKE LOWER(:query)
                OR LOWER(address) LIKE LOWER(:query)   
                OR LOWER(month) LIKE LOWER(:query)
                OR LOWER(organization) LIKE LOWER(:query)
                OR LOWER(publisher) LIKE LOWER(:query)
            ORDER BY id DESC
        """),
        {"query": f"%{query.lower()}%"}
    )

    inproceedings = [Inproceedings(**row._asdict()) for row in res.fetchall()]

    res = db.session.execute(
        text("""
            SELECT *
            FROM manuals
            WHERE
                LOWER(title) LIKE LOWER(:query)
                OR CAST(year AS TEXT) LIKE :query
                OR LOWER(author) LIKE LOWER(:query)
                OR LOWER(organization) LIKE LOWER(:query)
                OR LOWER(address) LIKE LOWER(:query)
                OR LOWER(edition) LIKE LOWER(:query)
                OR LOWER(month) LIKE LOWER(:query)
                OR LOWER(note) LIKE LOWER(:query)
            ORDER BY id DESC
        """),
        {"query": f"%{query.lower()}%"}
    )

    manuals = [Manual(**row._asdict()) for row in res.fetchall()]

    return articles + books + inproceedings + manuals

def reset_db():
    db_helper.reset_db()
