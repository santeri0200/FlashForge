from config import db
from sqlalchemy import text

def add_article(author, title, journal, year):
    sql = text("INSERT INTO articles (author, title, journal, year) VALUES (:author, :title, :journal, :year)")
    db.session.execute(sql, {"author": author, "title": title, "journal": journal, "year": year})
    db.session.commit()
    return True

def get_all_articles():
    sql = text("SELECT author, title, journal, year FROM articles")
    res = db.session.execute(sql)

    articles = res.fetchall()    
    return articles
