# Musical Tracks Many to One

This application will read an iTunes library in comma-separated-values (CSV) format and produce properly normalized tables as specified below. Once you have placed the proper data in the tables, press the button below to check your answer.

---

## Step 1: Create the tables

Done using "itune_tables.sql" file. Using

```sh
pg4e_232debcf0e=> \i itune_tables.sql
```

to create the tables.

## Step 2: Read the file and insert the data

Using the "\copy" command to read the data from "library.csv" file and insert it into "track_raw" table.

```sh
pg4e_232debcf0e=> \copy track_raw (title, artist, album, count, rating, len) FROM 'library.csv' WITH DELIMITER ',' CSV;
COPY 296
```

Checking if data is inserted into "track_raw" table.

```sh
pg4e_232debcf0e=> SELECT title, artist, count FROM track_raw LIMIT 5;
           title            |    artist    | count
----------------------------+--------------+-------
 Another One Bites The Dust | Queen        |    55
 Asche Zu Asche             | Rammstein    |    79
 Beauty School Dropout      | Various      |    48
 Black Dog                  | Led Zeppelin |   109
 Bring The Boys Back Home   | Pink Floyd   |    33
(5 rows)
```

## Step 3: Insert distinct albums into **album** table

```sql
INSERT INTO album (title) SELECT DISTINCT album FROM track_raw;
```

```sh
pg4e_232debcf0e=> INSERT INTO album (title) SELECT DISTINCT album FROM track_raw;
INSERT 0 41
pg4e_232debcf0e=> SELECT id, title FROM album LIMIT 5;
 id |            title
----+------------------------------
 42 | Onion News Network, Season 1
 43 | The Legend Of Johnny Cash
 44 | Peanut Butter and Jam
 45 | Who's Next
 46 | Greatest Hits
(5 rows)
```

## Step 4: Update the **album_id** column in **track_raw** table with the corresponding **id** from **album** table

```sql
UPDATE track_raw SET album_id = (SELECT album.id FROM album WHERE album.title = track_raw.album);
```

```sh
pg4e_232debcf0e=> UPDATE track_raw SET album_id = (SELECT album.id FROM album WHERE album.title = track_raw.album);
UPDATE 296
pg4e_232debcf0e=> SELECT title, album, album_id FROM track_raw LIMIT 20;
                  title                  |        album        | album_id
-----------------------------------------+---------------------+----------
 Another One Bites The Dust              | Greatest Hits       |       46
 Asche Zu Asche                          | Herzeleid           |       57
 Beauty School Dropout                   | Grease              |       53
 Black Dog                               | IV                  |       76
 Bring The Boys Back Home                | The Wall [Disc 2]   |       49
 Circles                                 | Blues Is            |       78
 Comfortably Numb                        | The Wall [Disc 2]   |       49
 Crazy Little Thing Called Love          | Greatest Hits       |       46
 Electric Funeral                        | Paranoid            |       51
 Fat Bottomed Girls                      | Greatest Hits       |       46
 For Those About To Rock (We Salute You) | Who Made Who        |       54
 Four Sticks                             | IV                  |       76
 Furious Angels                          | The Matrix Reloaded |       80
 Gelle                                   | Blues Is            |       78
 Going To California                     | IV                  |       76
 Grease                                  | Grease              |       53
 Hand of Doom                            | Paranoid            |       51
 Hells Bells                             | Who Made Who        |       54
 Hey You                                 | The Wall [Disc 2]   |       49
 I Worry                                 | Blues Is            |       78
(20 rows)
```

## Step 5: Insert data from **track_raw** to **track** table

```sql
INSERT INTO track (title, len, album_id) SELECT title, len, album_id FROM track_raw;
```

```sh
pg4e_232debcf0e=> INSERT INTO track (title, len, album_id) SELECT title, len, album_id FROM track_raw;
INSERT 0 296
pg4e_232debcf0e=> SELECT * FROM track LIMIT 10;
 id |             title              | len | rating | count | album_id
----+--------------------------------+-----+--------+-------+----------
  1 | Another One Bites The Dust     | 217 |        |       |       46
  2 | Asche Zu Asche                 | 231 |        |       |       57
  3 | Beauty School Dropout          | 239 |        |       |       53
  4 | Black Dog                      | 296 |        |       |       76
  5 | Bring The Boys Back Home       |  87 |        |       |       49
  6 | Circles                        | 355 |        |       |       78
  7 | Comfortably Numb               | 384 |        |       |       49
  8 | Crazy Little Thing Called Love | 163 |        |       |       46
  9 | Electric Funeral               | 293 |        |       |       51
 10 | Fat Bottomed Girls             | 257 |        |       |       46
(10 rows)
```
