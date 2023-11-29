"""
CREATE TABLE shelter_pets (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    animal_id   TEXT (256) UNIQUE,
    name        TEXT (256),
    animal_type TEXT (256),
    breed       TEXT (256),
    color       TEXT (256)
);
"""
"""
CREATE TABLE intakes (
    id               INTEGER    PRIMARY KEY AUTOINCREMENT,
    animal_id        TEXT (256) REFERENCES shelter_pets (animal_id),
    date_time        TEXT (256),
    found_location   TEXT (256),
    intake_type      TEXT (256),
    intake_condition TEXT (256),
    sex_upon_intake  TEXT (256),
    age_upon_intake  REAL 
);
"""
"""
CREATE TABLE outcomes (
    id               INTEGER    PRIMARY KEY AUTOINCREMENT,
    animal_id        TEXT (256) REFERENCES shelter_pets (animal_id),
    date_time        TEXT (256),
    outcome_type     TEXT (256),
    outcome_subtype  TEXT (256),
    sex_upon_outcome TEXT (256),
    age_upon_outcome REAL
);
"""