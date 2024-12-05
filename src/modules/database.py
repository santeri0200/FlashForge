# pylint: disable=redefined-builtin, bare-except
# pylint: disable=too-many-arguments, too-many-positional-arguments
from config import db
from sqlalchemy import text

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

def delete_article(id):
    try:
        sql = text("DELETE FROM articles WHERE id=:id")
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
    return articles

def reset_db():
    print("Clearing contents from table articles")
    sql = text("DELETE FROM articles")
    db.session.execute(sql)
    db.session.commit()
