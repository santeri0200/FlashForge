# pylint: disable=redefined-builtin, bare-except
from config import db
from sqlalchemy import text

def add_article(author, title, journal, year):
    try:
        sql = text("INSERT INTO articles (author, title, journal, year) VALUES (:author, :title, :journal, :year)")
        db.session.execute(sql, {"author": author, "title": title, "journal": journal, "year": year})
    except:
        return False
    db.session.commit()
    return True

def edit_article(id, author, title, journal, year):
    try:
        sql = text("UPDATE articles SET author=:author, title=:title, journal=:journal, year=:year WHERE id=:id")
        db.session.execute(sql, {"author": author, "title": title, "journal": journal, "year": year, "id":id})
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
    sql = text("SELECT id, author, title, journal, year FROM articles ORDER BY id DESC")
    res = db.session.execute(sql)

    articles = res.fetchall()
    return articles

def article_from_id(id):
    sql = text(f"SELECT id, author, title, journal, year FROM articles WHERE id={id} LIMIT 1")
    res = db.session.execute(sql)
    article = res.fetchone()
    return article

def search_result(query):
    if query is None:
        return []

    res = db.session.execute(
        text("""
            SELECT author, title, journal, year
            FROM articles
            WHERE
                author LIKE :query
                OR title LIKE :query
                OR journal LIKE :query
                OR CAST(year as TEXT) LIKE :query
            ORDER BY id DESC
        """),
        { "query": f"%{query}%" }
    )

    articles = res.fetchall()
    return articles

def reset_db():
    print("Clearing contents from table articles")
    sql = text("DELETE FROM articles")
    db.session.execute(sql)
    db.session.commit()
