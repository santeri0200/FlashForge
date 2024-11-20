from config import app, db
from sqlalchemy import text

table_name = "articles"
def table_exists(name):
    sql = text("""SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = :name)""")
    res = db.session.execute(sql, { "name": name })

    return res.fetchall()[0][0]

def reset_db():
    sql = text(f"""DELETE FROM {table_name}""")
    db.session.execute(sql)
    db.session.commit()

def setup_db():
    if table_exists(table_name):
        print(f"""Table {table_name} exists, dropping!""")
        sql = text(f"""DROP TABLE {table_name}""")
        db.session.execute(sql)
        db.session.commit()

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

if __name__ == "__main__":
    with app.app_context():
        setup_db()
