# Notes on A bit of Demo on Reading and Parsing Files

---

In one of the previous example we made a database by removing vertical replication. By normalizing the data.

Here we will convert a csv file to a normalized database.

**`SELECT` narrows your data down. Here you can use distinct and other operators. This helps us to narrow down the data.**

---

## Creating and Loading a Database

---

Suppose we have three table many to many relationship. We have account, post and comment.

```sql
CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    email VARCHAR(128) UNIQUE,
    created_at DATE NOT NULL DEFAULT NOW(),
    updated_at DATE NOT NULL DEFAULT NOW()
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) UNIQUE NOT NULL,
    content VARCHAR(1024),
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES post(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE fav (
    id SERIAL PRIMARY KEY,
    oops TEXT,
    post_id INTEGER REFERENCES post(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES account(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (post_id, account_id)
);
```

### Let's use `ALTER TABLE` to modify schema

#### Changing the data type of column `content` in `post` table from `VARCHAR(1024)` to `TEXT`

```sql
ALTER TABLE post ALTER COLUMN content TYPE TEXT;
```

#### Dropping a column from a table. Dropping the `oops` column from `fav` table

```sql
ALTER TABLE fav DROP COLUMN oops;
```

#### Adding a new column to a table. Adding a `howmuch` INTEGER column to `fav` table

```sql
ALTER TABLE fav ADD COLUMN howmuch INTEGER;
```

Now schema of the database is set.

### Let's Insert Some Data

```sh
demo_file_to_db=# \i inserting_data.sql
DELETE 0
ALTER SEQUENCE
ALTER SEQUENCE
ALTER SEQUENCE
ALTER SEQUENCE
INSERT 0 3
INSERT 0 3
INSERT 0 5
demo_file_to_db=# SELECT * FROM post;
 id |     title     |      content      | account_id |          created_at           |          updated_at
----+---------------+-------------------+------------+-------------------------------+-------------------------------
  1 | Dictionaries  | Are fun           |          3 | 2026-04-21 14:22:38.632123+00 | 2026-04-21 14:22:38.632123+00
  2 | BeautifulSoup | Has a complex API |          1 | 2026-04-21 14:22:38.632123+00 | 2026-04-21 14:22:38.632123+00
  3 | Many to Many  | Is elegant        |          2 | 2026-04-21 14:22:38.632123+00 | 2026-04-21 14:22:38.632123+00
(3 rows)
```

`inserting_data.sql` file contains the insert statements to insert data into the tables.

---

## Load data from csv file `03-Techniques.csv` to a Database

---

### Download the csv file `03-Techniques.csv` from the course materials and save it in your local machine

Content of the csv file is:

```csv
Zap,A
Zip,A
One,B
Two,B
```

### First Create The required tables

```sql
DROP TABLE IF EXISTS xy_raw;
DROP TABLE IF EXISTS y;
DROP TABLE IF EXISTS xy;

CREATE TABLE xy_raw(x TEXT, y TEXT, y_id INTEGER);
CREATE TABLE y (id SERIAL, PRIMARY KEY(id), y TEXT);
CREATE TABLE xy(id SERIAL, PRIMARY KEY(id), x TEXT, y_id INTEGER, UNIQUE(x,y_id));
```

Now the schema is

```sh
csv_to_db=# \d xy_raw
               Table "public.xy_raw"
 Column |  Type   | Collation | Nullable | Default
--------+---------+-----------+----------+---------
 x      | text    |           |          |
 y      | text    |           |          |
 y_id   | integer |           |          |
```

```sh
csv_to_db=# \d+ y
                                                       Table "public.y"
 Column |  Type   | Collation | Nullable |            Default            | Storage  | Compression | Stats target | Description
--------+---------+-----------+----------+-------------------------------+----------+-------------+--------------+-------------
 id     | integer |           | not null | nextval('y_id_seq'::regclass) | plain    |             |              |
 y      | text    |           |          |                               | extended |             |              |
Indexes:
    "y_pkey" PRIMARY KEY, btree (id)
Access method: heap
```

### Copy data from csv file to `xy_raw` db

```sh
csv_to_db=# \copy xy_raw(x, y) FROM '03-Techniques.csv' WITH DELIMITER ',' CSV;
COPY 4
```

Let's check if data is loaded.

```sh
csv_to_db=# SELECT * FROM xy_raw;
  x  | y | y_id
-----+---+------
 Zap | A |
 Zip | A |
 One | B |
 Two | B |
(4 rows)
```

So it is loaded.

### Let's load distinct values of `y` from `xy_raw` to `y` table

```sh
csv_to_db=# INSERT INTO y (y) SELECT DISTINCT y FROM xy_raw ORDER BY y;
INSERT 0 2
csv_to_db=# SELECT * FROM y;
 id | y
----+---
  1 | A
  2 | B
(2 rows)
```

`INSERT INTO y (y) SELECT DISTINCT y FROM xy_raw ORDER BY y;` statement inserts distinct values of `y` from `xy_raw` table to `y` table in ascending order.
It looks like a subquery but it is not. It is a `SELECT` statement that is used to insert data into another table.

### Now we have to update `y_id` column in `xy_raw` table with the corresponding `id` from `y` table

We can run the following query to update `y_id` column in `xy_raw` table with the corresponding `id` from `y` table.

```sql
UPDATE xy_raw SET y_id = (SELECT y.id FROM y WHERE y.y = xy_raw.y);
```

```sh
csv_to_db=# UPDATE xy_raw SET y_id = (SELECT y.id FROM y WHERE y.y = xy_raw.y);
UPDATE 4
csv_to_db=# SELECT * FROM xy_raw;
  x  | y | y_id
-----+---+------
 Zap | A |    1
 Zip | A |    1
 One | B |    2
 Two | B |    2
(4 rows)
```

Now `xy_raw` , `y_id` column has been updated with correct corresponding ids from `y` table.

### Now let's insert data from `xy_raw` to `xy` table

Following query can be used to update the table.

```sql
INSERT INTO xy (x, y_id) SELECT x, y_id FROM xy_raw;
```

```sh
csv_to_db=# INSERT INTO xy (x, y_id) SELECT x, y_id FROM xy_raw;
INSERT 0 4
csv_to_db=# SELECT * FROM xy;
 id |  x  | y_id
----+-----+------
  1 | Zap |    1
  2 | Zip |    1
  3 | One |    2
  4 | Two |    2
(4 rows)
```

So now we have two normalized tables `xy` and `y`

### Let's get back the original data using `JOIN`

SQL query which can be used is

```sql
SELECT * FROM xy JOIN y ON xy.y_id = y.id;
```

Or to get the exact data

```sql
SELECT xy.x, y.y FROM xy JOIN y ON xy.y_id = y.id;
```

```sh
csv_to_db=# SELECT * FROM xy JOIN y ON xy.y_id = y.id;
 id |  x  | y_id | id | y
----+-----+------+----+---
  1 | Zap |    1 |  1 | A
  2 | Zip |    1 |  1 | A
  3 | One |    2 |  2 | B
  4 | Two |    2 |  2 | B
(4 rows)

csv_to_db=# SELECT xy.x, y.y FROM xy JOIN y ON xy.y_id = y.id;
  x  | y
-----+---
 Zap | A
 Zip | A
 One | B
 Two | B
(4 rows)
```
