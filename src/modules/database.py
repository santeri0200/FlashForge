# pylint: disable=redefined-builtin, bare-except
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from sqlalchemy import text
from tests import db_helper
from entities.reference import Article, Book, Inproceedings, Manual

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
    del details['type']
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

def get_all_articles():
    sql = text("""
        SELECT *
        FROM articles
        ORDER BY id DESC
    """)
    res = db.session.execute(sql)

    # This should throw
    if not res:
        return []

    articles = [Article(**row._asdict()) for row in res.fetchall()]
    return articles

def article_from_id(id):
    sql = text("""
        SELECT *
        FROM articles
        WHERE id=:id LIMIT 1
    """)
    res = db.session.execute(sql, { "id": id })

    article = Article(**res.fetchone()._asdict())
    return article

def get_all_books():
    sql = text("SELECT * FROM Books ORDER BY id DESC")
    res = db.session.execute(sql)

    # This should throw
    if not res:
        return []

    books = [Book(**row._asdict()) for row in res.fetchall()]
    return books

def get_all_inproceedings():
    sql = text("SELECT * FROM Inproceedings ORDER BY id DESC")
    res = db.session.execute(sql)

    # This should throw
    if not res:
        return []

    inproceedings = [Inproceedings(**row._asdict()) for row in res.fetchall()]
    return inproceedings

def get_all_manuals():
    sql = text("SELECT * FROM Manuals ORDER BY id DESC")
    res = db.session.execute(sql)

    # This should throw
    if not res:
        return []

    inproceedings = [Manual(**row._asdict()) for row in res.fetchall()]
    return inproceedings


def ref_from_id(ref_type, id):
    table_names = {
        "article": "Articles",
        "book": "Books",
        "inproceedings": "Inproceedings",
        "manual": "Manual",
    }

    sql = text(f"SELECT * FROM {table_names[ref_type]} WHERE id={id} LIMIT 1")
    res = db.session.execute(sql)
    ref = res.fetchone()
    return ref

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

    articles = res.fetchall()

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

    books = res.fetchall()

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

    inproceedings = res.fetchall()

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

    manuals = res.fetchall()

    return articles, books, inproceedings, manuals

def reset_db():
    db_helper.reset_db()
