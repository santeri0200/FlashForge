# pylint: disable=redefined-builtin, bare-except
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from sqlalchemy import text
from tests import db_helper
from entities.reference import Article, Book

def add_reference(ref_type, ref):
    if ref.type == "article" and add_article(ref):
        return True
    elif ref.type == "book" and add_book(ref):
        return True

    return False

def add_article(ref):
    try:
        sql = text("""
            INSERT INTO articles
            VALUES (DEFAULT, :author, :title, :journal, :year, :volume, :number, :pages, :month, :note)
        """)
        db.session.execute(sql, ref.details())
    except:
        return False
    db.session.commit()
    return True

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

def add_book(ref):
    try:
        sql = text("INSERT INTO books (author, year, title, publisher, address) VALUES (:author, :year, :title, :publisher, :address)")
        db.session.execute(sql, ref.details())
    except:
        return False
    db.session.commit()
    return True

def edit_ref(ref_type, id, details):
    table_names = {
        "article": "articles",
        "book": "books"
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
        "book": "Books"
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

def ref_from_id(ref_type, id):
    table_names = {
        "article": "Articles",
        "book": "Books"
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
                author LIKE :query
                OR title LIKE :query
                OR journal LIKE :query
                OR CAST(year as TEXT) LIKE :query
                OR volume != NULL
                OR CAST(volume as TEXT) LIKE :query
                OR CAST(number as TEXT) LIKE :query
                OR pages LIKE :query
                OR month LIKE :query
                OR note LIKE :query
            ORDER BY id DESC
        """),
        { "query": f"%{query}%" }
    )

    articles = res.fetchall()

    res = db.session.execute(
        text("""
             SELECT *
            FROM Books
            WHERE
                author LIKE :query
                OR title LIKE :query
                OR publisher LIKE :query
                OR address LIKE :query
                OR CAST(year as TEXT) LIKE :query
             ORDER BY id DESC
         """),
         { "query": f"%{query}%" }
    )

    books = res.fetchall()
    return articles, books

def reset_db():
    db_helper.reset_db()
