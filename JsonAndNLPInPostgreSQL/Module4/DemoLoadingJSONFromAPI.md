# Notes on Loading JSON from an Star Wars API

---

## We will be using the [Star Wars API](https://swapi.info/api/) to load JSON data into PostgreSQL

## Python code for this is in [star_wars_api.py](./star_wars_api.py)

## On running the python program `python swapi.py`, 207 rows are inserted into the `swapi` table in PostgreSQL

---

## Running Queries on the `swapi` table

---

### Get `url` from body jsonb

#### Get first url from body jsonb

```sql
json_pg=# SELECT body->>'url' FROM swapi LIMIT 1;
              ?column?
-------------------------------------
 https://swapi.py4e.com/api/films/1/
(1 row)
```

#### Get 'url' where directory is 'George Lucas'

```sh
json_pg=# SELECT body->>'url' FROM swapi WHERE body @> '{"director": "George Lucas"}';
              ?column?
-------------------------------------
 https://swapi.py4e.com/api/films/1/
 https://swapi.py4e.com/api/films/4/
 https://swapi.py4e.com/api/films/5/
 https://swapi.py4e.com/api/films/6/
(4 rows)
```

#### Explain query plan for above query

```sh
json_pg=# explain SELECT body->>'url' FROM swapi WHERE body @> '{"director": "George Lucas"}';
                        QUERY PLAN
-----------------------------------------------------------
 Seq Scan on swapi  (cost=0.00..22.59 rows=1 width=32)
   Filter: (body @> '{"director": "George Lucas"}'::jsonb)
(2 rows)
```

---

## Create Index

---

### First put some race car data in the `swapi` table

**This is done to force the db to use indexes for the queries instead of doing a sequential scan.**

```sql
INSERT INTO swapi (body)
SELECT ('{"type": "Neon", "series": "24 Hours of Lemons", "number": ' || generate_series(1000, 5000) || '}')::jsonb;
```

### Create a GIN index on the `body` column with jsonb path ops

```sql
CREATE INDEX swapi_gin ON swapi USING GIN (body jsonb_path_ops);
```

```sh
json_pg=# \d+ swapi;
                                                                  Table "public.swapi"
   Column   |           Type           | Collation | Nullable |              Default              | Storage  | Compression | Stats target | Description
------------+--------------------------+-----------+----------+-----------------------------------+----------+-------------+--------------+-------------
 id         | integer                  |           | not null | nextval('swapi_id_seq'::regclass) | plain    |             |              |
 url        | character varying(2048)  |           |          |                                   | extended |             |              |
 status     | integer                  |           |          |                                   | plain    |             |              |
 body       | jsonb                    |           |          |                                   | extended |             |              |
 created_at | timestamp with time zone |           | not null | now()                             | plain    |             |              |
 updated_at | timestamp with time zone |           |          |                                   | plain    |             |              |
Indexes:
    "swapi_gin" gin (body jsonb_path_ops)
    "swapi_url_key" UNIQUE CONSTRAINT, btree (url)
Access method: heap
```

---

## After Index Queries

---

### Get 'url' where director is 'George Lucas'

```sh
json_pg=# explain SELECT body->>'url' FROM swapi WHERE body @> '{"director": "George Lucas"}';
                               QUERY PLAN
-------------------------------------------------------------------------
 Bitmap Heap Scan on swapi  (cost=12.82..16.83 rows=1 width=32)
   Recheck Cond: (body @> '{"director": "George Lucas"}'::jsonb)
   ->  Bitmap Index Scan on swapi_gin  (cost=0.00..12.82 rows=1 width=0)
         Index Cond: (body @> '{"director": "George Lucas"}'::jsonb)
(4 rows)
```

This time the query plan shows that the database is using the GIN index to find the relevant rows instead of doing a sequential scan on the entire table. This should result in a much faster query execution time, especially as the size of the table grows.

### Get 'url' of films where director is Not George Lucas

```sql
SELECT body->>'url' FROM swapi WHERE NOT(body @> '{"director": "George Lucas"}'::jsonb);
```

But this will return all the urls even of people and other categories. than files.

#### We can do better by using AND operator

```sh
json_pg=# SELECT body->>'url' FROM swapi
WHERE NOT(body @> '{"director": "George Lucas"}'::jsonb)
AND body->>'url' LIKE 'https://swapi.py4e.com/api/films/%';
              ?column?
-------------------------------------
 https://swapi.py4e.com/api/films/2/
 https://swapi.py4e.com/api/films/3/
 https://swapi.py4e.com/api/films/7/
(3 rows)
```

```sql
EXPLAIN SELECT body->>'url' FROM swapi
WHERE NOT(body @> '{"director": "George Lucas"}'::jsonb)
AND body->>'url' LIKE 'https://swapi.py4e.com/api/films/%';
```

```sh
json_pg=# EXPLAIN SELECT body->>'url' FROM swapi
WHERE NOT(body @> '{"director": "George Lucas"}'::jsonb)
AND body->>'url' LIKE 'https;//swapi.py4e.com/api/films/%';
                                                                  QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------
 Seq Scan on swapi  (cost=0.00..150.69 rows=21 width=32)
   Filter: ((NOT (body @> '{"director": "George Lucas"}'::jsonb)) AND ((body ->> 'url'::text) ~~ 'https;//swapi.py4e.com/api/films/%'::text))
(2 rows)
```

---

## Let's modify the JSONB

---

Let's add a type field to the JSONB

### Get the type field from the JSONB

```sql
--get the type
SELECT ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }') FROM swapi LIMIT 1;
```

```sh
json_pg=# SELECT ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }') FROM swapi LIMIT 1;
      ?column?
--------------------
 {"type": "films" }
(1 row)
```

### Convert the above query to return a JSONB instead of text

```sql
SELECT ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }')::jsonb FROM swapi LIMIT 1;
```

### Merge new json back into the body

```sql
SELECT body || ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }')::jsonb FROM swapi LIMIT 1;
```

### Update all the rows with type field

```sql
UPDATE swapi SET body = body || ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }')::jsonb;
```

```sh
json_pg=# UPDATE swapi SET body = body || ('{"type": "' || substring(body->>'url', 'https://swapi.py4e.com/api/([a-z]+)/') || '" }')::jsonb;
UPDATE 4208
```

### Let's check if we can make a where clause on the new type field

```sql
json_pg=# SELECT body->>'type' AS type, body->>'url' AS url, body->>'name' AS name  FROM swapi WHERE body @> '{"type": "species"}' LIMIT 10;
  type   |                  url                   |      name
---------+----------------------------------------+----------------
 species | https://swapi.py4e.com/api/species/1/  | Human
 species | https://swapi.py4e.com/api/species/2/  | Droid
 species | https://swapi.py4e.com/api/species/3/  | Wookiee
 species | https://swapi.py4e.com/api/species/4/  | Rodian
 species | https://swapi.py4e.com/api/species/5/  | Hutt
 species | https://swapi.py4e.com/api/species/34/ | Muun
 species | https://swapi.py4e.com/api/species/6/  | Yoda's species
 species | https://swapi.py4e.com/api/species/7/  | Trandoshan
 species | https://swapi.py4e.com/api/species/8/  | Mon Calamari
 species | https://swapi.py4e.com/api/species/9/  | Ewok
(10 rows)
```

### Explain query plan for same query

```sql
json_pg=# explain SELECT body->>'type' AS type, body->>'url' AS url, body->>'name' AS name FROM swapi WHERE body @> '{"type": "species"}' LIMIT 10;
                                   QUERY PLAN
--------------------------------------------------------------------------------
 Limit  (cost=13.02..34.06 rows=10 width=96)
   ->  Bitmap Heap Scan on swapi  (cost=13.02..92.97 rows=38 width=96)
         Recheck Cond: (body @> '{"type": "species"}'::jsonb)
         ->  Bitmap Index Scan on swapi_gin  (cost=0.00..13.01 rows=38 width=0)
               Index Cond: (body @> '{"type": "species"}'::jsonb)
(5 rows)
```

It is a very efficient query because it is using the GIN index to find the relevant rows instead of doing a sequential scan on the entire table.

---

## Now we can shorten our query of the films where director is George Lucas

---

### Films where director is George Lucas

```sql
json_pg=# SELECT url FROM swapi WHERE body @> '{"director": "George Lucas", "type": "films"}';
                 url
-------------------------------------
 https://swapi.py4e.com/api/films/1/
 https://swapi.py4e.com/api/films/4/
 https://swapi.py4e.com/api/films/5/
 https://swapi.py4e.com/api/films/6/
(4 rows)
```

### Films where director is Not George Lucas

```sql
SELECT url FROM swapi WHERE body @> '{"type": "films"}' AND NOT(body @> '{"director": "George Lucas"}');
```

```sh
json_pg=# SELECT url FROM swapi WHERE body @> '{"type": "films"}' AND NOT(body @> '{"director": "George Lucas"}');
                 url
-------------------------------------
 https://swapi.py4e.com/api/films/2/
 https://swapi.py4e.com/api/films/3/
 https://swapi.py4e.com/api/films/7/
(3 rows)
```

### Explain query plan

```sql
json_pg=# explain SELECT url FROM swapi WHERE body @> '{"type": "films"}' AND NOT(body @> '{"director": "George Lucas"}');
                               QUERY PLAN
-------------------------------------------------------------------------
 Bitmap Heap Scan on swapi  (cost=12.82..16.83 rows=1 width=38)
   Recheck Cond: (body @> '{"type": "films"}'::jsonb)
   Filter: (NOT (body @> '{"director": "George Lucas"}'::jsonb))
   ->  Bitmap Index Scan on swapi_gin  (cost=0.00..12.82 rows=1 width=0)
         Index Cond: (body @> '{"type": "films"}'::jsonb)
(5 rows)
```

We can see that the query plan is using the GIN index to find the relevant rows based on the type field, and then filtering out the rows where the director is George Lucas. This should be much faster than doing a sequential scan on the entire table.
