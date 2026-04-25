# Notes on Text in Databases and Text Functions

---

## Text in Databases

---

### Generating Test Data

- We can't really explore performance if we only have 5 records.
- So before we play a bit with performance we need to make up some data.

**We can use postgres built in functions to generate random data.**

- We use `repeat()` to generate long strings (horizontal);
- We use `generate_series()` to generate lots of rows (vertical).
  - Like Python's `range()`
- We use `random()` to make rows unique
  - Floating point `0 <= random() <= 1.0`

#### Let's look at some examples for individual use

##### `random()`

```sh
discuss=# SELECT random(), random(), trunc(random()*100);
      random       |       random       | trunc
-------------------+--------------------+-------
 0.880146611907678 | 0.4108503027568575 |     5
(1 row)
```

##### `repeat()`

```sh
discuss=# SELECT repeat('Neon ', 5);
          repeat
---------------------------
 Neon Neon Neon Neon Neon
(1 row)
```

##### `generate_series()`

```sh
discuss=# SELECT generate_series(1, 5);
 generate_series
-----------------
               1
               2
               3
               4
               5
(5 rows)
```

We can combine these functions to generate a lot of data:

### Let's see an example of combining these function to generate data

```sql
SELECT 'https://sql4e.com/neon/' || trunc(random()*1000000) || repeat('Lemon', 5) || generate_series(1, 5);
```

```sh
discuss=# SELECT 'https://sql4e.com/neon/' || trunc(random()*1000000) || repeat('Lemon', 5) || generate_series(1, 5);
                        ?column?
---------------------------------------------------------
 https://sql4e.com/neon/630236LemonLemonLemonLemonLemon1
 https://sql4e.com/neon/455925LemonLemonLemonLemonLemon2
 https://sql4e.com/neon/334784LemonLemonLemonLemonLemon3
 https://sql4e.com/neon/534980LemonLemonLemonLemonLemon4
 https://sql4e.com/neon/156816LemonLemonLemonLemonLemon5
(5 rows)
```

You can see that `generate_series(1, 5)` is generating 5 rows, which forces the other functions to generate 5 different values for each row.

---

## Text Functions

---

### Many Text Functions

#### Where Clause Operators

- `LIKE / ILIKE / NOT LIKE / NOT ILIKE`: `LIKE` is case sensitive, `ILIKE` is case insensitive. You can use `%` as a wildcard for any sequence of characters and `_` as a wildcard for a single character. For example some sql queries using `LIKE` and `ILIKE`:

```sql
SELECT 'Neon' LIKE 'Ne%'; -- true
SELECT 'Neon' LIKE 'Ne_'; -- false
SELECT 'Neon' LIKE 'Ne__'; -- true
SELECT 'Neon' ILIKE 'ne%'; -- true
SELECT 'Neon' ILIKE 'ne_'; -- false
SELECT 'Neon' ILIKE 'ne__'; -- true
-- NOT LIKE examples
SELECT 'Neon' NOT LIKE 'Ne%'; -- false
SELECT 'NEON' NOT ILIKE 'ne%'; -- false
```

- `SIMILAR TO / NOT SIMILAR TO`: Similar to `LIKE` but with more powerful pattern matching using regular expressions. For example:

```sql
SELECT 'Neon' SIMILAR TO 'N(e|a)on'; -- true
SELECT 'Neon' SIMILAR TO 'N(e|a)on|N(e|a)on'; -- true
SELECT 'Neon' SIMILAR TO 'N(e|a)on|N(e|a)on'; -- true
```

- `= > < >= <= BETWEEN IN`: Standard comparison operators that can be used with text. For example:

```sql
SELECT 'Neon' = 'Neon'; -- true
SELECT 'Neon' > 'Ne'; -- true (lexicographical order)
SELECT 'Neon' < 'Neop'; -- true
SELECT 'Neon' >= 'Neon'; -- true
SELECT 'Neon' <= 'Neop'; -- true
SELECT 'Neon' BETWEEN 'Ne' AND 'Neop'; -- true
SELECT 'Neon' IN ('Ne', 'Neon', 'Neop'); -- true
```

#### Manipulate SELECT Results / WHERE Clause

- `lower()`: Converts a string to lowercase. For example:

```sql
SELECT lower('Neon'); -- 'neon'
```

- `upper()`: Converts a string to uppercase. For example:

```sql
SELECT upper('Neon'); -- 'NEON'
```

### Let's create a table and play with some of these functions

```sql
CREATE TABLE textfun ( content TEXT );
CREATE INDEX textfun_b ON textfun (content);
```

```sh
discuss=# CREATE TABLE textfun ( content TEXT );
CREATE INDEX textfun_b ON textfun (content);
CREATE TABLE
CREATE INDEX
discuss=# SELECT pg_relation_size('textfun'), pg_indexes_size('textfun');
 pg_relation_size | pg_indexes_size
------------------+-----------------
                0 |            8192
(1 row)
```

- `CREATE INDEX` creates a B-tree index on the `content` column.
- As you can see index is already taking up space, that is whole idea of index. Some overhead in space to speed up queries.

```sql
INSERT INTO textfun (content)
SELECT (CASE WHEN (random() < 0.5)
         THEN 'https://www.pg4e.com/neon/'
         ELSE 'http://www.pg4e.com/Lemons/'
         END) || generate_series(100000, 200000);
```

```sh
discuss=# INSERT INTO textfun (content)
SELECT (CASE WHEN (random() < 0.5)
         THEN 'https://www.pg4e.com/neon/'
         ELSE 'http://www.pg4e.com/Lemons/'
         END) || generate_series(100000, 200000);
INSERT 0 100001
discuss=# SELECT pg_relation_size('textfun'), pg_indexes_size('textfun');
 pg_relation_size | pg_indexes_size
------------------+-----------------
          6832128 |         8282112
(1 row)
```

- `CASE WHEN` is used to randomly generate URLs starting with either 'https://www.pg4e.com/neon/' or 'http://www.pg4e.com/Lemons/'.
- `CASE WHEN... THEN... ELSE... END` is a conditional expression that evaluates the condition and returns the corresponding result based on whether the condition is true or false.
- In this case you can see that index grows faster than data, this is because in this case the row is TEXT and index is B-tree, so index has to store the whole string for each row, which takes more space than the actual data.

### Some other queries using TEXT Functions

```sql
SELECT content FROM textfun WHERE content LIKE '%150000%';
SELECT upper(content) FROM textfun WHERE content LIKE '%150000%';
SELECT lower(content) FROM textfun WHERE content LIKE '%150000%';
SELECT right(content, 4) FROM textfun WHERE content LIKE '%150000%';
SELECT left(content, 4) from textfun where content like '%150000%';
```

```sh
discuss=# SELECT content FROM textfun WHERE content LIKE '%150000%';
             content
----------------------------------
 https://www.pg4e.com/neon/150000
(1 row)

discuss=# SELECT upper(content) FROM textfun WHERE content LIKE '%150000%';
              upper
----------------------------------
 HTTPS://WWW.PG4E.COM/NEON/150000
(1 row)

discuss=# SELECT lower(content) FROM textfun WHERE content LIKE '%150000%';
              lower
----------------------------------
 https://www.pg4e.com/neon/150000
(1 row)

discuss=# SELECT right(content, 4) FROM textfun WHERE content LIKE '%150000%';
 right
-------
 0000
(1 row)

discuss=# SELECT left(content, 4) from textfun where content like '%150000%';
 left
------
 http
(1 row)
```

### Some more text functions

```sql
SELECT strpos(content, 'ttps://') FROM textfun WHERE content LIKE '%150000%';
SELECT substr(content, 2, 4) FROM textfun WHERE content LIKE '%150000%';
SELECT split_part(content, '/', 3) FROM textfun WHERE content LIKE '%150000%';
SELECT translate(content, 'th.p/', 'TH!P_') FROM textfun WHERE content LIKE '%150000%';
```

- `strpos(string, substring)`: Returns the position of the first occurrence of `substring` in `string`. For example:

```sql
discuss=# SELECT strpos(content, 'ttps://') FROM textfun WHERE content LIKE '%150000%';
 strpos
--------
      2
(1 row)
```

- `substr(string, start, length)`: Returns a substring of `string` starting at position `start` with the specified `length`. For example:

```sql
discuss=# SELECT substr(content, 2, 4) FROM textfun WHERE content LIKE '%150000%';
 substr
--------
 ttps
(1 row)
```

- `split_part(string, delimiter, field)`: Splits `string` using `delimiter` and returns the specified `field`. For example:

```sql
discuss=# SELECT split_part(content, '/', 3) FROM textfun WHERE content LIKE '%150000%';
  split_part
--------------
 www.pg4e.com
(1 row)
```

- `translate(string, from, to)`: Translates characters in `string` from `from` to `to`. For example:

```sql
discuss=# SELECT translate(content, 'th.p/', 'TH!P_') FROM textfun WHERE content LIKE '%150000%';
            translate
----------------------------------
 HTTPs:__www!Pg4e!com_neon_150000
(1 row)
```

`t` is replaced with `T`, `h` is replaced with `H`, `.` is replaced with `!`, `p` is replaced with `P`, and `/` is replaced with `_`.

---

## Let's do some performance analysis using `explain analyze`

---

### Looking for as a prefix

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content LIKE 'racing%';
                                              QUERY PLAN
------------------------------------------------------------------------------------------------------
 Seq Scan on textfun  (cost=0.00..2084.01 rows=10 width=33) (actual time=4.459..4.460 rows=0 loops=1)
   Filter: (content ~~ 'racing%'::text)
   Rows Removed by Filter: 100001
 Planning Time: 0.057 ms
 Execution Time: 4.473 ms
(5 rows)
```

### Looking for _racing_ anywhere in the string

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content LIKE '%racing%';
                                              QUERY PLAN
------------------------------------------------------------------------------------------------------
 Seq Scan on textfun  (cost=0.00..2084.01 rows=10 width=33) (actual time=7.124..7.125 rows=0 loops=1)
   Filter: (content ~~ '%racing%'::text)
   Rows Removed by Filter: 100001
 Planning Time: 0.060 ms
 Execution Time: 7.136 ms
(5 rows)
```

### Case insensitive prefix search

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content ILIKE 'racing%';
                                               QUERY PLAN
--------------------------------------------------------------------------------------------------------
 Seq Scan on textfun  (cost=0.00..2084.01 rows=10 width=33) (actual time=45.988..45.988 rows=0 loops=1)
   Filter: (content ~~* 'racing%'::text)
   Rows Removed by Filter: 100001
 Planning Time: 0.117 ms
 Execution Time: 46.000 ms
(5 rows)
```

---

## When we create index with `text_pattern_ops` we can speed up prefix search

**`text_pattern_ops`** is a special operator class for B-tree indexes that allows for efficient pattern matching with `LIKE` and `ILIKE` when the pattern is a prefix (i.e., it does not start with a wildcard). When you create an index on a text column using `text_pattern_ops`, it optimizes the index for these types of queries.

```sql
DROP INDEX textfun_b;
CREATE INDEX textfun_b ON textfun (content text_pattern_ops);
```

Then doing prefix search again:

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content LIKE 'racing%';
                                                        QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------
 Index Only Scan using textfun_b on textfun  (cost=0.42..4.44 rows=10 width=33) (actual time=0.046..0.046 rows=0 loops=1)
   Index Cond: ((content ~>=~ 'racing'::text) AND (content ~<~ 'racinh'::text))
   Filter: (content ~~ 'racing%'::text)
   Heap Fetches: 0
 Planning Time: 0.213 ms
 Execution Time: 0.057 ms
(6 rows)
```

---

## Some optimization notes

---

### Sequential scans can be improved by adding a LIMIT clause

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content LIKE '%150000%';
                                              QUERY PLAN
------------------------------------------------------------------------------------------------------
 Seq Scan on textfun  (cost=0.00..2084.01 rows=10 width=33) (actual time=5.239..9.835 rows=1 loops=1)
   Filter: (content ~~ '%150000%'::text)
   Rows Removed by Filter: 100000
 Planning Time: 0.066 ms
 Execution Time: 9.846 ms
(5 rows)

discuss=# explain analyze SELECT content FROM textfun WHERE content LIKE '%150000%' LIMIT 1;
                                                 QUERY PLAN
------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.00..208.40 rows=1 width=33) (actual time=3.949..3.951 rows=1 loops=1)
   ->  Seq Scan on textfun  (cost=0.00..2084.01 rows=10 width=33) (actual time=3.948..3.948 rows=1 loops=1)
         Filter: (content ~~ '%150000%'::text)
         Rows Removed by Filter: 50000
 Planning Time: 0.064 ms
 Execution Time: 3.960 ms
(6 rows)
```

- Adding a `LIMIT` clause can significantly reduce the execution time of a query that would otherwise require a full sequential scan, especially when the desired result is found early in the scan. In this example, the execution time dropped from 9.846 ms to 3.960 ms when we added `LIMIT 1`, because it stopped scanning after finding the first match, rather than scanning through all 100,000 rows.

### Let's use IN clause with and without subqueries

#### When using IN with a list of values

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content IN ('http://www.pg4e.com/neon/150000', 'https://www.pg4e.com/neon/150000');
                                                       QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------
 Index Only Scan using textfun_b on textfun  (cost=0.42..8.87 rows=2 width=33) (actual time=0.143..0.144 rows=1 loops=1)
   Index Cond: (content = ANY ('{http://www.pg4e.com/neon/150000,https://www.pg4e.com/neon/150000}'::text[]))
   Heap Fetches: 0
 Planning Time: 0.061 ms
 Execution Time: 0.155 ms
(5 rows)
```

#### When using IN with a subquery

```sh
discuss=# explain analyze SELECT content FROM textfun WHERE content IN (SELECT content FROM textfun WHERE content LIKE '%150000%');
                                                          QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------
 Nested Loop  (cost=2084.45..2128.59 rows=10 width=33) (actual time=10.402..10.405 rows=1 loops=1)
   ->  HashAggregate  (cost=2084.04..2084.14 rows=10 width=33) (actual time=10.386..10.387 rows=1 loops=1)
         Group Key: textfun_1.content
         Batches: 1  Memory Usage: 24kB
         ->  Seq Scan on textfun textfun_1  (cost=0.00..2084.01 rows=10 width=33) (actual time=5.241..10.379 rows=1 loops=1)
               Filter: (content ~~ '%150000%'::text)
               Rows Removed by Filter: 100000
   ->  Index Only Scan using textfun_b on textfun  (cost=0.42..4.44 rows=1 width=33) (actual time=0.013..0.014 rows=1 loops=1)
         Index Cond: (content = textfun_1.content)
         Heap Fetches: 0
 Planning Time: 1.123 ms
 Execution Time: 10.428 ms
(12 rows)
```
