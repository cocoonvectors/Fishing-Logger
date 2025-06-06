-- CREATE TABLE species (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL UNIQUE,
--     common_name TEXT NULL,
--     lang TEXT NULL,
--     region TEXT NULL
-- );

-- -- trips 
-- CREATE TABLE trips (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     species_id INTEGER NOT NULL,
--     latlong TEXT NOT NULL,
--     location TEXT NOT NULL,
--     date  TEXT NOT NULL,
--     time TEXT NOT NULL,
--     temperature REAL NOT NULL,
--     cloud_cover TEXT NOT NULL,
--     humidity REAL NOT NULL,
--     wind_speed REAL NOT NULL,
--     lunar_phase TEXT NOT NULL,
--     FOREIGN KEY (species_id) REFERENCES species(id)
-- );

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
