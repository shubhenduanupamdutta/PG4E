# Notes on Index Choices and Techniques in PostgreSQL

---

## Let's build an application, a hypothetical _Web Crawler_

---

### Approach

- Retrieve a web page from our queue of web pages.
- Store the web page and look for outgoing links.
- Add the links _we have not already read_ to a queue.

### This table will be large and we will look up URLs quite often (100s per retrieved page)

---

## How long is a URL?

---

- In real world, URLs can be very long. So we can't make it a `VARCHAR`
- What if we make URL a `TEXT` field and index it? Index size will be large and lookups will be slow. So what can we do?

**We can index a hash of the URL instead of the URL itself.**

```sql
CREATE TABLE cr2 (
    id SERIAL,
    url TEXT,
    content TEXT
);

CREATE UNIQUE INDEX cr2_md5 on cr2 (md5(url));
```

```sh
pg4e=# CREATE TABLE cr2 (
    id SERIAL,
    url TEXT,
    content TEXT
);
CREATE TABLE
pg4e=# CREATE UNIQUE INDEX cr2_md5 on cr2 (md5(url));
CREATE INDEX
pg4e=# INSERT INTO cr2 (url)
pg4e-# SELECT repeat('Neon', 1000) || generate_series(1, 5000);
INSERT 0 5000
pg4e=# SELECT pg_relation_size('cr2'), pg_indexes_size('cr2');
 pg_relation_size | pg_indexes_size
------------------+-----------------
           507904 |          376832
(1 row)
```

### When we query for equality with direct text, index is not used

```sh
pg4e=# explain SELECT * FROM cr2 WHERE url='lemons';
                      QUERY PLAN
------------------------------------------------------
 Seq Scan on cr2  (cost=0.00..124.50 rows=1 width=99)
   Filter: (url = 'lemons'::text)
(2 rows)
```

### When we query for equality with the hash, index is used, and look up is fast

```sh
pg4e=# explain SELECT * FROM cr2 WHERE md5(url) = md5('lemons');
                             QUERY PLAN
---------------------------------------------------------------------
 Index Scan using cr2_md5 on cr2  (cost=0.28..8.30 rows=1 width=99)
   Index Cond: (md5(url) = '238ad51a7f1d25d991e6b51879d6b66d'::text)
(2 rows)
```

### Comparing using `explain analyze` shows that the hash-based lookup is much faster

```sh
pg4e=# explain analyze SELECT * FROM cr2 WHERE md5(url) = md5('lemons');
                                                  QUERY PLAN
--------------------------------------------------------------------------------------------------------------
 Index Scan using cr2_md5 on cr2  (cost=0.28..8.30 rows=1 width=99) (actual time=0.016..0.017 rows=0 loops=1)
   Index Cond: (md5(url) = '238ad51a7f1d25d991e6b51879d6b66d'::text)
 Planning Time: 0.077 ms
 Execution Time: 0.026 ms
(4 rows)

pg4e=# explain analyze SELECT * FROM cr2 WHERE url='lemons';
                                           QUERY PLAN
------------------------------------------------------------------------------------------------
 Seq Scan on cr2  (cost=0.00..124.50 rows=1 width=99) (actual time=0.307..0.307 rows=0 loops=1)
   Filter: (url = 'lemons'::text)
   Rows Removed by Filter: 5000
 Planning Time: 0.045 ms
 Execution Time: 0.318 ms
(5 rows)
```

---

## Using additional column of hash value for faster lookups

---

**We can add an additional column to store the hash value of the URL and index that column. This way, we can quickly look up the hash value and then retrieve the corresponding URL. Here uuid type is very useful, since its width is same as that of md5 hash.**

### Creating table with and additional hash column for indexing

```sql
CREATE TABLE cr3 (
    id SERIAL,
    url TEXT,
    url_md5 uuid UNIQUE,
    content TEXT
);
```

Unique index on `url_md5` is automatically created since it is declared as `UNIQUE`.

```sh
discuss=# CREATE TABLE cr3 (
    id SERIAL,
    url TEXT,
    url_md5 uuid UNIQUE,
    content TEXT
);
CREATE TABLE
discuss=# \d+ cr3
                                                        Table "public.cr3"
 Column  |  Type   | Collation | Nullable |             Default             | Storage  | Compression | Stats target | Description
---------+---------+-----------+----------+---------------------------------+----------+-------------+--------------+-------------
 id      | integer |           | not null | nextval('cr3_id_seq'::regclass) | plain    |             |              |
 url     | text    |           |          |                                 | extended |             |              |
 url_md5 | uuid    |           |          |                                 | plain    |             |              |
 content | text    |           |          |                                 | extended |             |              |
Indexes:
    "cr3_url_md5_key" UNIQUE CONSTRAINT, btree (url_md5)
Access method: heap
```

### Inserting data into the table with hash column

```sql
discuss=# INSERT INTO cr3 (url)
SELECT repeat('Neon', 1000) || generate_series(1, 5000);
INSERT 0 5000
discuss=# UPDATE cr3 SET url_md5 = md5(url)::uuid;
UPDATE 5000
```

### Checking index size

```sh
discuss=# SELECT pg_relation_size('cr3'), pg_indexes_size('cr3');
 pg_relation_size | pg_indexes_size
------------------+-----------------
          1097728 |          270336
(1 row)
```

### Querying with `explain analyze` shows that lookups are fast

```sh
discuss=# explain analyze SELECT * FROM cr3 WHERE url_md5=md5('lemons')::uuid;
                                                      QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------
 Index Scan using cr3_url_md5_key on cr3  (cost=0.28..8.30 rows=1 width=115) (actual time=0.005..0.005 rows=0 loops=1)
   Index Cond: (url_md5 = '238ad51a-7f1d-25d9-91e6-b51879d6b66d'::uuid)
 Planning Time: 0.163 ms
 Execution Time: 0.013 ms
(4 rows)
```

---

## Comparing Index Strategies

---

### 1. No Index, comparing with sequential scan

- **Relation Size**: 507904 bytes
- **Index Size**: 0 bytes
- **SELECT Execution Time**: 0.318 ms

### 2. Indexing the hash of the URL

- **Relation Size**: 507904 bytes
- **Index Size**: 376832 bytes
- **SELECT Execution Time**: 0.026 ms

### 3. Adding an additional column for hash and indexing it

- **Relation Size**: 1097728 bytes
- **Index Size**: 270336 bytes
- **SELECT Execution Time**: 0.013 ms

Depending on the use case, we can choose the appropriate indexing strategy. If we have a large number of URLs and need fast lookups, adding an additional column for the hash and indexing it may be the best option. However, if storage space is a concern, indexing the hash of the URL directly may be more efficient.

---

## PostgreSQL Index Types

---

### B-Tree Indexes

- Maintains Order
- Usually Preferred
- Helps on exact lookup, prefix lookup, <, >, range, sort

### Hash Indexes

- Smaller - helps only on exact lookup
- Not recommended before PostgreSQL 10

---

## Creating Hash Indexes

---

```sql
CREATE TABLE cr4 (
    id SERIAL,
    url TEXT,
    content TEXT
);
```

and then inserting default data

```sql
discuss=# INSERT INTO cr4 (url)
SELECT repeat('Neon', 1000) || generate_series(1, 5000
);
INSERT 0 5000
```

Now we can create a hash index on the `url` column

```sql
CREATE INDEX cr4_hash ON cr4 USING hash (url);
```

```sh
discuss=# SELECT pg_relation_size('cr4'), pg_indexes_size('cr4');
 pg_relation_size | pg_indexes_size
------------------+-----------------
           507904 |          278528
(1 row)
```

Using explain analyze to check if the hash index is used for lookups

```sh
discuss=# explain analyze SELECT * FROM cr4 WHERE url='lemons';
                                                  QUERY PLAN
---------------------------------------------------------------------------------------------------------------
 Index Scan using cr4_hash on cr4  (cost=0.00..8.02 rows=1 width=99) (actual time=0.007..0.007 rows=0 loops=1)
   Index Cond: (url = 'lemons'::text)
 Planning Time: 0.094 ms
 Execution Time: 0.015 ms
(4 rows)
```

This is a very small index and very fast look up.
