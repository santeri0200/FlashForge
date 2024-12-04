CREATE TABLE IF NOT EXISTS Articles (
    id SERIAL PRIMARY KEY,
    -- Required fields
    author  TEXT NOT NULL,
    title   TEXT NOT NULL,
    journal TEXT NOT NULL,
    year    INT  NOT NULL,
    -- Optional fields
    volume  INT,
    number  INT,
    pages   TEXT,
    month   TEXT,
    note    TEXT,

    UNIQUE (author, title)
);
