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

def get_all_articles():
    sql = text("SELECT author, title, journal, year FROM articles ORDER BY id DESC")
    res = db.session.execute(sql)

    articles = res.fetchall()    
    return articles

def reset_db():
    print(f"Clearing contents from table articles")
    sql = text(f"DELETE FROM articles")
    db.session.execute(sql)
    db.session.commit()