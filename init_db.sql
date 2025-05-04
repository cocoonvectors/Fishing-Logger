CREATE TABLE species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    common_name TEXT NULL,
    region TEXT NULL
);

-- trips 
CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    datetime  TEXT NOT NULL,
    temperature REAL NOT NULL,
    cloud_cover TEXT NOT NULL,
    humidity REAL NOT NULL,
    wind_speed REAL NOT NULL,
    lunar_phase TEXT NOT NULL,
    solar_phase TEXT NOT NULL,
    FOREIGN KEY (species_id) REFERENCES species(id)
);