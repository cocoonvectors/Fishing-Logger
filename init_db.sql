CREATE TABLE species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    common_name TEXT NULL,
    lang TEXT NULL,
    region TEXT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    species_id INTEGER NOT NULL,
    latlong TEXT NOT NULL,
    location TEXT NOT NULL,
    date  TEXT NOT NULL,
    time TEXT NOT NULL,
    temperature REAL NOT NULL,
    cloud_cover TEXT NOT NULL,
    humidity REAL NOT NULL,
    wind_speed REAL NOT NULL,
    lunar_phase TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (species_id) REFERENCES species(id)
);


