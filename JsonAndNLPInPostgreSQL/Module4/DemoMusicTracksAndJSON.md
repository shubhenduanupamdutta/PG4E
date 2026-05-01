# Demo: Music Tracks and JSON

---

## Download the dataset

```bash
wget https://www.pg4e.com/code/library.jstxt
```

This dataset contains information about music tracks in JSON format. Each line in the file is a JSON object representing a music track with various attributes such as name, artist, album, genre, and more.

---

## Create a table to store the JSON data

```sql
DROP TABLE IF EXISTS jtrack;
CREATE TABLE jtrack (
    id SERIAL PRIMARY KEY,
    body JSONB
);
```

```sh
json_pg=# \d+ jtrack
                                                       Table "public.jtrack"
 Column |  Type   | Collation | Nullable |              Default               | Storage  | Compression | Stats target | Description
--------+---------+-----------+----------+------------------------------------+----------+-------------+--------------+-------------
 id     | integer |           | not null | nextval('jtrack_id_seq'::regclass) | plain    |             |              |
 body   | jsonb   |           |          |                                    | extended |             |              |
Indexes:
    "jtrack_pkey" PRIMARY KEY, btree (id)
Access method: heap
```

---

## Load the JSON data into the table

```bash
\copy jtrack (body) FROM 'library.jstxt' WITH CSV QUOTE E'\x01' DELIMITER E'\x02';
```

```sh
json_pg=# \copy jtrack (body) FROM 'library.jstxt' WITH CSV QUOTE E'\x01' DELIMITER E'\x02';
COPY 318
json_pg=# SELECT id, body FROM jtrack LIMIT 2;
 id |                                                               body
----+-----------------------------------------------------------------------------------------------------------------------------------
  1 | {"name": "Another One Bites The Dust", "album": "Greatest Hits", "count": 55, "artist": "Queen", "length": 217103, "rating": 100}
  2 | {"name": "Asche Zu Asche", "album": "Herzeleid", "count": 79, "artist": "Rammstein", "length": 231810, "rating": 100}
(2 rows)
```

### Let's check the type of the `body` column

```sql
json_pg=# SELECT pg_typeof(body) FROM jtrack LIMIT 1;
 pg_typeof
-----------
 jsonb
(1 row)
```

---

## Querying JSON data

---

### Get the name of the track as a text field

```sql
SELECT body->>'name' FROM jtrack LIMIT 5;
```

```sh
json_pg=# SELECT body->>'name' FROM jtrack LIMIT 5;
          ?column?
----------------------------
 Another One Bites The Dust
 Asche Zu Asche
 Beauty School Dropout
 Black Dog
 Bring The Boys Back Home
(5 rows)
```

### Types returned from JSONB operators

Could we use parentheses and cast convert to text?

```sql
SELECT pg_typeof(body->'name') FROM jtrack LIMIT 1; -- 1
SELECT pg_typeof(body->'name'::text) FROM jtrack LIMIT 1; -- 2
SELECT pg_typeof(body->'name')::text FROM jtrack LIMIT 1; -- 3
SELECT pg_typeof((body->'name')::text) FROM jtrack LIMIT 1; -- 4
```

```sh
json_pg=# SELECT pg_typeof(body->'name') FROM jtrack LIMIT 1; -- 1
SELECT pg_typeof(body->'name'::text) FROM jtrack LIMIT 1; -- 2
SELECT pg_typeof(body->'name')::text FROM jtrack LIMIT 1; -- 3
SELECT pg_typeof((body->'name')::text) FROM jtrack LIMIT 1; -- 4
 pg_typeof
-----------
 jsonb
(1 row)

 pg_typeof
-----------
 jsonb
(1 row)

 pg_typeof
-----------
 jsonb
(1 row)

 pg_typeof
-----------
 text
(1 row)
```

1. The first query returns `jsonb` because the `->` operator returns a JSONB value.
2. The second query also returns `jsonb` because the cast to `text` is applied on `body` before the `->` operator is applied, which does not change the type of the result of the `->` operator.
3. The third query returns `jsonb` because the cast to `text` is applied to the result of the `pg_typeof` function, which is still a JSONB value'
4. The fourth query returns `text` because the cast to `text` is applied to the result of the `->` operator, which converts the JSONB value to text before it is returned.

#### But why even go through all this trouble? Why not just use the `->>` operator which directly returns text?

```sql
SELECT pg_typeof(body->>'name') FROM jtrack LIMIT 1;
```

### This returns maximum count of the tracks

```sql
SELECT MAX((body->>'count')::int) FROM jtrack;
```

```sh
json_pg=# SELECT MAX((body->>'count')::int) FROM jtrack;
 max
-----
 463
(1 row)
```

You have to make sure to cast the value to `int` before using the `MAX` function, otherwise it will return the maximum value as a string, which is not what we want.

```sh
json_pg=# SELECT MAX(body->>'count') FROM jtrack;
 max
-----
 93
(1 row)
```

### Order by the count of the tracks

```sql
SELECT body->>'name' AS name FROM jtrack ORDER BY (body->>'count')::int DESC LIMIT 5;
```

```sh
json_pg=# SELECT body->>'name' AS name FROM jtrack ORDER BY (body->>'count')::int DESC LIMIT 5;
      name
----------------
 Mother Joy
 The Arrow
 Aguas De Marco
 Banana Bay
 Dulaman
(5 rows)
```

### Casting to int from JSONB Fragment

```sql
SELECT (body->'count')::int AS count FROM jtrack ORDER BY count DESC LIMIT 5;
```

```sh
json_pg=# SELECT (body->'count')::int AS count FROM jtrack ORDER BY count DESC LIMIT 5;
 count
-------
   463
   416
   407
   403
   403
(5 rows)
```

### Look into JSON for a value

```sql
SELECT count(*) FROM jtrack WHERE body->>'name' = 'Summer Nights';
```

```sh
json_pg=# SELECT count(*) FROM jtrack WHERE body->>'name' = 'Summer Nights';
 count
-------
     1
(1 row)
```

### Ask if the body contains a key-value pair

```sql
SELECT count(*) FROM jtrack WHERE body @> '{"name": "Summer Nights"}';
```

```sh
json_pg=# SELECT count(*) FROM jtrack WHERE body @> '{"name": "Summer Nights"}';
 count
-------
     1
(1 row)
```

### Adding something to the JSONB column

```sql
UPDATE jtrack SET body = body || '{"favorite": "yes"}' WHERE (body->'count')::int > 200;
```

```sh
json_pg=# UPDATE jtrack SET body = body || '{"favorite": "yes"}' WHERE (body->'count')::int > 200;
UPDATE 33
```

```sh
son_pg=# SELECT * FROM jtrack WHERE (body->'count')::int>400 LIMIT 2;
 id  |                                                                             body
-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------
 118 | {"name": "Mother Joy", "album": "Natural Wonders Music Sampler 1999", "count": 463, "artist": "Matt Ender", "length": 287294, "rating": 0, "favorite": "yes"}
 120 | {"name": "Dulaman", "album": "Natural Wonders Music Sampler 1999", "count": 403, "artist": "Altan", "length": 223007, "rating": 0, "favorite": "yes"}
(2 rows)
```

### Give me count of tracks where a key exists in the JSONB column

```sql
SELECT count(*) FROM jtrack WHERE body ? 'favorite';
```

```sh
json_pg=# SELECT count(*) FROM jtrack WHERE body ? 'favorite';
 count
-------
    33
(1 row)
```

---

## Indexes on JSONB

---

### Insert large amount of data into the table

```sql
INSERT INTO jtrack (body)
SELECT ('{"type": "Neon", "series": "24 Hours of Lemons", "number": ' || generate_series(1000, 5000) || '}')::jsonb;
```

```sh
json_pg=# INSERT INTO jtrack (body)
SELECT ('{"type": "Neon", "series": "24 Hours of Lemons", "number": ' || generate_series(1000, 5000) || '}')::jsonb;
INSERT 0 4001
json_pg=# SELECT count(*) FROM jtrack;
 count
-------
  4319
(1 row)
```

### Prepare Three Indexes

```sql
DROP INDEX jtrack_btree;
DROP INDEX jtrack_gin;
DROP INDEX jtrack_gin_path_ops;

CREATE INDEX jtrack_btree ON jtrack USING BTREE ((body->>'name'));
CREATE INDEX jtrack_gin ON jtrack USING GIN (body);
CREATE INDEX jtrack_gin_path_ops ON jtrack USING GIN (body jsonb_path_ops);
```

```sh
json_pg=# \d+ jtrack;
                                                       Table "public.jtrack"
 Column |  Type   | Collation | Nullable |              Default               | Storage  | Compression | Stats target | Description
--------+---------+-----------+----------+------------------------------------+----------+-------------+--------------+-------------
 id     | integer |           | not null | nextval('jtrack_id_seq'::regclass) | plain    |             |              |
 body   | jsonb   |           |          |                                    | extended |             |              |
Indexes:
    "jtrack_pkey" PRIMARY KEY, btree (id)
    "jtrack_btree" btree ((body ->> 'name'::text))
    "jtrack_gin" gin (body)
    "jtrack_gin_path_ops" gin (body jsonb_path_ops)
Access method: heap
```

### Let's see which query hit which index

#### 1. Querying artist name using `->>` operator

```sql
EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body->>'artist' = 'Queen';
```

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body->>'artist' = 'Queen';
                          QUERY PLAN
---------------------------------------------------------------
 Aggregate  (cost=127.84..127.85 rows=1 width=8)
   ->  Seq Scan on jtrack  (cost=0.00..127.78 rows=22 width=0)
         Filter: ((body ->> 'artist'::text) = 'Queen'::text)
(3 rows)
```

**This was a sequential scan, which means it did not use any index.**

#### 2. Querying 'name' using `->>` operator

```sql
EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body->>'name' = 'Summer Nights';
```

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body->>'name' = 'Summer Nights';
                                    QUERY PLAN
----------------------------------------------------------------------------------
 Aggregate  (cost=49.54..49.55 rows=1 width=8)
   ->  Bitmap Heap Scan on jtrack  (cost=4.45..49.48 rows=22 width=0)
         Recheck Cond: ((body ->> 'name'::text) = 'Summer Nights'::text)
         ->  Bitmap Index Scan on jtrack_btree  (cost=0.00..4.45 rows=22 width=0)
               Index Cond: ((body ->> 'name'::text) = 'Summer Nights'::text)
(5 rows)
```

**This query used the btree index on the 'name' field, which is why it is much faster than the previous query.**

#### 3. Querying whether `favorite` key exists using `?` operator

```sql
EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body ? 'favorite';
```

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body ? 'favorite';
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Aggregate  (cost=16.83..16.84 rows=1 width=8)
   ->  Bitmap Heap Scan on jtrack  (cost=12.82..16.83 rows=1 width=0)
         Recheck Cond: (body ? 'favorite'::text)
         ->  Bitmap Index Scan on jtrack_gin  (cost=0.00..12.82 rows=1 width=0)
               Index Cond: (body ? 'favorite'::text)
(5 rows)
```

#### 4. Querying whether `body` contains a key-value pair using `@>` operator

```sql
EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body @> '{"name": "Summer Nights"}';
```

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body @> '{"name": "Summer Nights"}';
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Aggregate  (cost=16.83..16.84 rows=1 width=8)
   ->  Bitmap Heap Scan on jtrack  (cost=12.82..16.83 rows=1 width=0)
         Recheck Cond: (body @> '{"name": "Summer Nights"}'::jsonb)
         ->  Bitmap Index Scan on jtrack_gin_path_ops  (cost=0.00..12.82 rows=1 width=0)
               Index Cond: (body @> '{"name": "Summer Nights"}'::jsonb)
(5 rows)
```

**This query used the GIN index with jsonb_path_ops, which is optimized for queries that check if a JSONB column contains a specific key-value pair.**

Some other queries which will use the GIN index with jsonb_path_ops:

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body @> '{"artist": "Queen"}';
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Aggregate  (cost=16.83..16.84 rows=1 width=8)
   ->  Bitmap Heap Scan on jtrack  (cost=12.82..16.83 rows=1 width=0)
         Recheck Cond: (body @> '{"artist": "Queen"}'::jsonb)
         ->  Bitmap Index Scan on jtrack_gin_path_ops  (cost=0.00..12.82 rows=1 width=0)
               Index Cond: (body @> '{"artist": "Queen"}'::jsonb)
(5 rows)
```

#### 5. Querying whether `body` contains multiple key-value pairs using `@>` operator

```sql
EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body @> '{"name": "Folsom Prison Blues", "artist": "Johnny Cash"}';
```

```sh
json_pg=# EXPLAIN SELECT COUNT(*) FROM jtrack WHERE body @> '{"name": "Folsom Prison Blues", "artist": "Johnny Cash"}';
                                              QUERY PLAN
-------------------------------------------------------------------------------------------------------
 Aggregate  (cost=25.53..25.54 rows=1 width=8)
   ->  Bitmap Heap Scan on jtrack  (cost=21.51..25.52 rows=1 width=0)
         Recheck Cond: (body @> '{"name": "Folsom Prison Blues", "artist": "Johnny Cash"}'::jsonb)
         ->  Bitmap Index Scan on jtrack_gin_path_ops  (cost=0.00..21.51 rows=1 width=0)
               Index Cond: (body @> '{"name": "Folsom Prison Blues", "artist": "Johnny Cash"}'::jsonb)
(5 rows)
```

---

## Updating JSONB data

---

### Incrementing the count of a track

Let's try some things

#### Adding directly to the JSONB value

```sql
SELECT (body->'count') + 1 FROM jtrack LIMIT 1;
```

```sh
json_pg=# SELECT (body->'count') + 1 FROM jtrack LIMIT 1;
ERROR:  operator does not exist: jsonb + integer
LINE 1: SELECT (body->'count') + 1 FROM jtrack LIMIT 1;
                               ^
HINT:  No operator matches the given name and argument types. You might need to add explicit type casts.
```

Doesn't work because the `->` operator returns a JSONB value, and you cannot directly add an integer to a JSONB value.

#### Casting to int before adding

```sql
SELECT (body->'count')::int + 1 FROM jtrack LIMIT 1;
```

```sh
json_pg=# SELECT (body->'count')::int + 1 FROM jtrack LIMIT 1;
 ?column?
----------
       56
(1 row)
```

This works because we are casting the JSONB value to an integer before adding 1 to it.

#### Using `->>` operator to get the value as text and then casting to int

```sh
json_pg=# SELECT ( (body->>'count')::int + 1) FROM jtrack WHERE body->>'name'='Summer Nights';
 ?column?
----------
       36
(1 row)
```

#### Finally, let's update the count of the track

```sql
UPDATE jtrack SET body = jsonb_set(body, '{ count }', ( (body->'count')::int + 1)::text::jsonb)
WHERE body->>'name' = 'Summer Nights';
```
