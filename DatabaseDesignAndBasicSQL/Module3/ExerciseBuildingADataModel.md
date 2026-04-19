# Exercise: Building a Database for a Music Library

---

## User Interface

---

The UI has these columns

- Track
- Album
- Artist
- Genre
- Rating
- Len
- Count

---

## Let's decide on Data Model

---

**Thing to note:** There is a relationship between data. Track belong to album and album belongs to artist.

Where does `genre` fit in? It is an attribute of track.
So `genre` belongs to the track.

**Let's build a simple data model for this.**

### First let's have a table for the tracks called `track`

- `title` can be one column in the `track` table
- `len` can be one column in the `track` table (length of the track in seconds)
- `count` can be one column in the `track` table (number of times the track has been played)
- `rating` can be one column in the `track` table (user rating of the track)
- `album_id` can be a foreign key in the `track` table that references the primary key of the `album` table (to indicate which album the track belongs to)
- `genre_id` can be a foreign key in the `track` table that references the primary key of the `genre` table (to indicate which genre the track belongs to)

### Let's have a table for albums `album`

- `id` can be the primary key for the `album` table
- `title` can be one column in the `album` table (title of the album)
- `artist_id` can be a foreign key in the `album` table that references the primary key of the `artist` table (to indicate which artist created the album)

### Let's have a table for artists `artist`

- `id` can be the primary key for the `artist` table
- `name` can be one column in the `artist` table (name of the artist)

### Since genre is a string and it can be repeated across tracks, we can have a separate table for genres `genre`

- `id` can be the primary key for the `genre` table
- `name` can be one column in the `genre` table (name of the genre)

**This is an example of many-to-one relationships. Many tracks belong to one album and many albums belong to one artist. Also many tracks can belong to one genre.**

---

## Building Tables

---

### Creating our Music Database

```sh
sudo -u postgres psql postgres
```

After connecting to database, we can create a new database for our music library:

```sh
postgres=# CREATE DATABASE music WITH OWNER 'pg4e' ENCODING 'UTF8';
CREATE DATABASE
postgres=#
```

### Creating the tables

```sql
CREATE TABLE artist (
    id SERIAL,
    name VARCHAR(128) UNIQUE,
    PRIMARY KEY (id)
);
```

```sql
CREATE TABLE album (
    id SERIAL,
    title VARCHAR(128) UNIQUE,
    artist_id INTEGER REFERENCES artist(id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);
```

`ON DELETE CASCADE` means that if an artist is deleted, all albums that reference that artist will also be deleted.
Similarly, there are other options like `ON DELETE SET NULL` which will set the foreign key to NULL if the referenced record is deleted, and `ON DELETE RESTRICT` which will prevent deletion of the referenced record if there are any records that reference it.

```sql
CREATE TABLE genre (
    id SERIAL,
    name VARCHAR(128) UNIQUE,
    PRIMARY KEY (id)
);
```

```sql
CREATE TABLE track (
    id SERIAL,
    title VARCHAR(128),
    len INTEGER,
    count INTEGER,
    rating INTEGER,
    album_id INTEGER REFERENCES album(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genre(id) ON DELETE SET NULL,
    UNIQUE (title, album_id),
    PRIMARY KEY (id)
);
```

`UNIQUE (title, album_id)` means that the combination of title and album_id must be unique in the track table. This allows us to have tracks with the same title as long as they belong to different albums, but prevents duplicate tracks within the same album.

---

## Inserting Data

---

### Inserting artists

```sh
music=> INSERT INTO artist (name) VALUES ('Led Zeppelin');
INSERT 0 1
music=> INSERT INTO artist (name) VALUES ('AC/DC');
INSERT 0 1
music=> SELECT * FROM artist;
 id |    name
----+-------------
  1 | Led Zeppelin
  2 | AC/DC
(2 rows)
```

### Inserting albums

```sh
music=> INSERT INTO album (title, artist_id) VALUES ('Who Made Who', 2);
INSERT 0 1
music=> INSERT INTO album (title, artist_id) VALUES ('IV', 1);
INSERT 0 1
music=> SELECT * FROM album;
 id |    title     | artist_id
----+--------------+-----------
  1 | Who Made Who |         2
  2 | IV           |         1
(2 rows)
```

### Inserting genres

```sh
music=> INSERT INTO genre (name) VALUES ('Rock');
INSERT 0 1
music=> INSERT INTO genre (name) VALUES ('Metal');
INSERT 0 1
music=> SELECT * FROM genre;
id |  name
----+-------
  1 | Rock
  2 | Metal
(2 rows)
```

### Inserting tracks

```sh
music=> INSERT INTO track (title, rating, len, count, album_id, genre_id) VALUES ('Black Dog', 5, 296, 10, 2, 1);
INSERT 0 1
music=> INSERT INTO track (title, rating, len, count, album_id, genre_id) VALUES ('Stairway to Heaven', 5, 482, 15, 2, 1);
INSERT 0 1
music=> INSERT INTO track (title, rating, len, count, album_id, genre_id) VALUES ('Who Made Who', 4, 210, 5, 1, 2);
INSERT 0 1
music=> INSERT INTO track (title, rating, len, count, album_id, genre_id) VALUES ('For Those About to Rock', 4, 340, 8, 1, 1);
INSERT 0 1
music=> SELECT * FROM track;
    id |        title            | len | count | rating | album_id | genre_id
-------+-------------------------+-----+-------+--------+----------+----------
     1 | Black Dog               | 296 |    10 |      5 |        2 |        1
     2 | Stairway to Heaven      | 482 |    15 |      5 |        2 |        1
     3 | Who Made Who            | 210 |     5 |      4 |        1 |        2
     4 | For Those About to Rock | 340 |     8 |      4 |        1 |        1
(4 rows)
```

**We have relationships!**

---

## Extracting Data for Viewing

---

### Let's say we want to see album name and corresponding artist name

```sh
music=> SELECT album.title, artist.name
FROM album JOIN artist ON album.artist_id = artist.id;
       title        |       name
--------------------+--------------------
 Who Made Who       | AC/DC
    IV                 | Led Zeppelin
```

Same when we also want to see the ids connecting them

```sh
music=> SELECT album.title, album.artist_id, artist.id, artist.name
FROM album JOIN artist ON album.artist_id = artist.id;
       title        | artist_id | id |       name
--------------------+-----------+----+--------------------
 Who Made Who       |         2 |  2 | AC/DC
IV                  |         1 |  1 | Led Zeppelin
```

### Let's say we want to see track title, artist name, album title and genre name

```sh
music=> SELECT track.title, album.title, artist.name, genre.name
FROM track
JOIN album ON track.album_id = album.id
JOIN artist ON album.artist_id = artist.id
JOIN genre ON track.genre_id = genre.id;
        title         |       title        |       name        |  name
----------------------+--------------------+-------------------+-----------------------
 Black Dog            | IV                 | Led Zeppelin      | Rock
 Stairway to Heaven   | IV                 | Led Zeppelin      | Rock
 About to Rock        | Who Made Who       | AC/DC             | Metal
 Who Made Who         | Who Made Who       | AC/DC             | Metal
```
