from config import app, db
from sqlalchemy import text

table_name = "articles"
def table_exists(name):
    sql = text(f"""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{name}');""")
    res = db.session.execute(sql)

    return res.fetchall()[0][0]

def reset_db(name):
    sql = text(f"""DELETE FROM {name};""")
    db.session.execute(sql)
    db.session.commit()

def drop_table(name):
    print(f"""Dropping table {name}!""")
    sql = text(f"""DROP TABLE {name}""")
    db.session.execute(sql)
    db.session.commit()

def create_table(name):
    print(f"""Creating table {table_name}""")
    sql = text(f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            -- Required fields
            author  TEXT NOT NULL,
            title   TEXT NOT NULL,
            journal TEXT NOT NULL,
            year    INT  NOT NULL,
            -- Optional fields
            volume  INT,
            number  INT,
            pages   INT,
            month   INT,
            note    TEXT,

            UNIQUE (author, title)
        )
    """)
    db.session.execute(sql)
    db.session.commit()

def setup_db():
    if table_exists(table_name):
        drop_table(table_name)
    create_table(table_name)

if __name__ == "__main__":
    with app.app_context():
        setup_db()
