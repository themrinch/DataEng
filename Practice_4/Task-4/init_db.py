"""
CREATE TABLE products (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    name        TEXT (256) UNIQUE,
    price       REAL,
    quantity    INTEGER,
    category    TEXT (256),
    fromCity    TEXT (256),
    isAvailable TEXT (256),
    views       INTEGER,
    version     INTEGER    DEFAULT (0)
);
"""