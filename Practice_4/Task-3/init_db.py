"""
CREATE TABLE songs (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    artist      TEXT (256),
    song        TEXT (256),
    duration_ms INTEGER,
    year        INTEGER,
    tempo       REAL,
    genre       TEXT (256),
    loudness    REAL
);
"""