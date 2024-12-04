# pylint: disable=redefined-builtin, bare-except
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from sqlalchemy import text

def add_reference(ref_type, *argv):
    if ref_type == "article":
        author, title, journal, year = argv[0], argv[1], argv[2], argv[3]
        if add_article(author, title, journal, year):
            return True
        return False

    if ref_type == "book":
        author, year, title, publisher, address = argv[0], argv[1], argv[2], argv[3], argv[4]
        if add_book(author, year, title, publisher, address):
            return True
        return False

def add_article(author, title, journal, year, volume, number, pages, month, note):
    try:
        sql = text("""
            INSERT INTO articles
            VALUES (DEFAULT, :author, :title, :journal, :year, :volume, :number, :pages, :month, :note)
        """)
        db.session.execute(sql, {
            "author": author,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "number": number,
            "pages": pages,
            "month": month,
            "note":note
        })
    except:
        return False
    db.session.commit()
    return True

def edit_article(id, author, title, journal, year, volume, number, pages, month, note):
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
        db.session.execute(sql, {
            "author": author,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "number": number,
            "pages": pages,
            "month": month,
            "note":note,
            "id":id
        })
    except:
        return False
    db.session.commit()
    return True

def add_book(author, year, title, publisher, address):
    try:
        sql = text("INSERT INTO books (author, year, title, publisher, address) VALUES (:author, :year, :title, :publisher, :address)")
        db.session.execute(sql, {"author": author, "year": year, "title": title, "publisher": publisher, "address": address})
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
    sql = text("SELECT * FROM articles ORDER BY id DESC")
    res = db.session.execute(sql)

    articles = res.fetchall()
    return articles

def article_from_id(id):
    sql = text("""
        SELECT id, author, title, journal, year, volume, number, pages, month, note
        FROM articles
        WHERE id=:id LIMIT 1
    """)
    res = db.session.execute(sql, { "id": id })
    article = res.fetchone()
    return article

def get_all_books():
    sql = text("SELECT * FROM Books ORDER BY id DESC")
    res = db.session.execute(sql)

    books = res.fetchall()
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
    print("Clearing contents from table articles")
    sql = text("DELETE FROM articles")
    db.session.execute(sql)
    db.session.commit()
