from config import db
from sqlalchemy import text

def add_article(author, title, journal, year):
    sql = text("INSERT INTO articles (author, title, journal, year) VALUES (:author, :title, :journal, :year)")
    db.session.execute(sql, {"author": author, "title": title, "journal": journal, "year": year})
    db.session.commit()
    return True