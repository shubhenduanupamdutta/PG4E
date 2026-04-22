DROP TABLE IF EXISTS category;
CREATE TABLE category (
  id SERIAL,
  name VARCHAR(128) UNIQUE,
  PRIMARY KEY(id)
);

DROP TABLE IF EXISTS iso;
CREATE TABLE iso (
  id SERIAL PRIMARY KEY,
  name CHAR(2) UNIQUE
);

DROP TABLE IF EXISTS state;
CREATE TABLE state (
  id SERIAL PRIMARY KEY,
  name VARCHAR(64) UNIQUE
);

DROP TABLE IF EXISTS region;
CREATE TABLE region (
  id SERIAL PRIMARY KEY,
  name VARCHAR(32) UNIQUE
);

DROP TABLE IF EXISTS justification;
CREATE TABLE justification (
    id SERIAL PRIMARY KEY,
    reason VARCHAR(4096) UNIQUE
);

DROP TABLE IF EXISTS unesco;
CREATE TABLE unesco (
    id SERIAL PRIMARY KEY,
    name VARCHAR(1024) UNIQUE,
    description TEXT,
    justification_id INTEGER REFERENCES justification(id) ON DELETE SET NULL,
    year INTEGER,
    longitude FLOAT, latitude FLOAT,
    area_hectares FLOAT,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL,
    iso_id INTEGER REFERENCES iso(id) ON DELETE SET NULL,
    state_id INTEGER REFERENCES state(id) ON DELETE SET NULL,
    region_id INTEGER REFERENCES region(id) ON DELETE SET NULL
);