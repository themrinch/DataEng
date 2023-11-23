"""
CREATE TABLE games (
    id           INTEGER    PRIMARY KEY AUTOINCREMENT,
    name         TEXT (256),
    city         TEXT (256),
    begin        TEXT (256),
    system       TEXT (256),
    tours_count  INTEGER,
    min_rating   INTEGER,
    time_on_game INTEGER
);
"""
"""
CREATE TABLE awards (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id         REFERENCES games (id),
    place   INTEGER,
    prise   INTEGER
);
"""
