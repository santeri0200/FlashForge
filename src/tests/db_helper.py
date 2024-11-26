from config import app, db
from sqlalchemy import text

TABLE_NAME = "articles"
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
    # pylint: disable=unused-argument
    print(f"""Creating table {TABLE_NAME}""")
    sql = text(f"""
        CREATE TABLE {TABLE_NAME} (
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
    if table_exists(TABLE_NAME):
        drop_table(TABLE_NAME)
    create_table(TABLE_NAME)

if __name__ == "__main__":
    with app.app_context():
        setup_db()
