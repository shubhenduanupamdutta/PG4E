# Assignment 3: Musical Tracks Database Plus Artists

---

This application will read an iTunes library in comma-separated-values (CSV) and produce properly normalized tables as specified below.

---

## Step 1: Download RAW data

In this case raw data is same as in Assignment 1. **library.csv**

---

## Step 2: Create Tables

### 1. **album** table

```sql
DROP TABLE IF EXISTS album CASCADE;
CREATE TABLE album (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) UNIQUE
);
```

```sh
pg4e_232debcf0e=> DROP TABLE IF EXISTS album CASCADE;
CREATE TABLE album (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) UNIQUE
);
NOTICE:  drop cascades to constraint track_album_id_fkey on table track
DROP TABLE
CREATE TABLE
```

### 2. **track** table

```sql
DROP TABLE IF EXISTS track CASCADE;
CREATE TABLE track (
    id SERIAL PRIMARY KEY,
    title TEXT,
    artist TEXT,
    album TEXT,
    album_id INTEGER REFERENCES album(id) ON DELETE CASCADE,
    count INTEGER,
    rating INTEGER,
    len INTEGER
);
```

```sh
pg4e_232debcf0e=> DROP TABLE IF EXISTS track CASCADE;
CREATE TABLE track (
    id SERIAL PRIMARY KEY,
    title TEXT,
    artist TEXT,
    album TEXT,
    album_id INTEGER REFERENCES album(id) ON DELETE CASCADE,
    count INTEGER,
    rating INTEGER,
    len INTEGER
);
DROP TABLE
CREATE TABLE
```

### 3. **artist** table

```sql
DROP TABLE IF EXISTS artist CASCADE;
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE
);
```

```sh
pg4e_232debcf0e=> DROP TABLE IF EXISTS artist CASCADE;
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE
);
NOTICE:  table "artist" does not exist, skipping
DROP TABLE
CREATE TABLE
```

### 4. **tracktoartist** table - This is the junction table for Many to Many relationship between track and artist

```sql
DROP TABLE IF EXISTS tracktoartist CASCADE;
CREATE TABLE tracktoartist (
    id SERIAL PRIMARY KEY,
    track VARCHAR(128),
    track_id INTEGER REFERENCES track(id) ON DELETE CASCADE,
    artist VARCHAR(128),
    artist_id INTEGER REFERENCES artist(id) ON DELETE CASCADE
);
```

```sh
pg4e_232debcf0e=> DROP TABLE IF EXISTS tracktoartist CASCADE;
CREATE TABLE tracktoartist (
    id SERIAL PRIMARY KEY,
    track VARCHAR(128),
    track_id INTEGER REFERENCES track(id) ON DELETE CASCADE,
    artist VARCHAR(128),
    artist_id INTEGER REFERENCES artist(id) ON DELETE CASCADE
);
NOTICE:  table "tracktoartist" does not exist, skipping
DROP TABLE
CREATE TABLE
```

---

## Step 3: Copy data from **library.csv** to **track** table

```sh
pg4e_232debcf0e=> \copy track(title, artist, album, count, rating, len) FROM 'library.csv' WITH DELIMITER ',' CSV;
COPY 296
```

---

## Step 4: Normalize the data

### 1. Populate **album** table with unique album names from **track** table and then update **track** table with corresponding `album_id`

```sql
INSERT INTO album (title) SELECT DISTINCT album FROM track;
UPDATE track SET album_id = (SELECT id FROM album WHERE album.title = track.album);
```

```sh
pg4e_232debcf0e=> INSERT INTO album (title) SELECT DISTINCT album FROM track;
UPDATE track SET album_id = (SELECT id FROM album WHERE album.title = track.album);
INSERT 0 41
UPDATE 296
```

### 2. Populate **tracktoartist** table with unique track and artist combinations from **track** table

```sql
INSERT INTO tracktoartist (track, artist) SELECT DISTINCT title, artist FROM track;
```

### 3. Populate **artist** table with unique artist names from **tracktoartist** table and then update **tracktoartist** table with corresponding `artist_id`

```sql
INSERT INTO artist (name) SELECT DISTINCT artist FROM tracktoartist;
UPDATE tracktoartist SET artist_id = (SELECT id FROM artist WHERE artist.name = tracktoartist.artist);
```

```sh
pg4e_232debcf0e=> INSERT INTO artist (name) SELECT DISTINCT artist FROM tracktoartist;
UPDATE tracktoartist SET artist_id = (SELECT id FROM artist WHERE artist.name = tracktoartist.artist);
INSERT 0 51
UPDATE 296
```

### 4. Update `track_id` in **tracktoartist** table with corresponding `id` from **track** table

```sql
UPDATE tracktoartist SET track_id = (SELECT id FROM track WHERE track.title = tracktoartist.track);
```

### 5. Alter table to drop columns with vertical replication of string if they are not needed anymore

```sql
ALTER TABLE track DROP COLUMN album; -- We can drop album column from track table as we have album_id which is the foreign key to album table
ALTER TABLE track DROP COLUMN artist; -- We can drop artist column from track table as we have artist_id which is the foreign key to artist table
ALTER TABLE tracktoartist DROP COLUMN track; -- We can drop track column from tracktoartist table as we have track_id which is the foreign key to track table
ALTER TABLE tracktoartist DROP COLUMN artist; -- We can drop artist column from tracktoartist table as we have artist_id which is the foreign key to artist table
```

```sh
pg4e_232debcf0e=> ALTER TABLE track DROP COLUMN album;
ALTER TABLE track DROP COLUMN artist;
ALTER TABLE tracktoartist DROP COLUMN track;
ALTER TABLE tracktoartist DROP COLUMN artist;
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
```
