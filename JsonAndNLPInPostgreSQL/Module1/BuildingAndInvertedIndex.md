# Notes of Building an Inverted Index in PostgreSQL

---

## Use of Inverted Indexes

---

### Similar to Google Search

- **Crawl**: Retrieve documents, parse them and create an inverted index, for quick searching.
- **Search**: Take keywords, find the documents with the words and then rank them and present results.

---

## Inverted Indexes - Using Only SQL

---

We can split long text columns into space-delimited words using PostgreSQL's split-like function called `string_to_array()`. And then we can use the PostgreSQL `unnest()` function to turn the resulting array into separate rows.

```sh
pg4e=# SELECT string_to_array('Hello world', ' ');
 string_to_array
-----------------
 {Hello,world}
(1 row)

pg4e=# SELECT unnest(string_to_array('Hello world', ' '));
 unnest
--------
 Hello
 world
(2 rows)
```

After that, it is just a few `SELECT DISTINCT` statements and we can create and use an inverted index.

Since, **Inverted index is just a mapping from a keyword to the rows that contain the keyword**.

```sh
natural_language=# CREATE TABLE docs (id SERIAL PRIMARY KEY, doc TEXT);
CREATE TABLE
natural_language=# INSERT INTO docs (doc) VALUES
('This is SQL and Python and other fun teaching stuff'),
('More people should learn SQL from UMSI'),
('UMSI also teaches Python and also SQL');
INSERT 0 3
natural_language=# CREATE TABLE docs_gin(keyword TEXT, doc_id INTEGER REFERENCES docs(id) ON DELETE CASCADE);
CREATE TABLE
natural_language=# SELECT * FROM docs;
 id |                         doc
----+-----------------------------------------------------
  1 | This is SQL and Python and other fun teaching stuff
  2 | More people should learn SQL from UMSI
  3 | UMSI also teaches Python and also SQL
(3 rows)
```

### Breaking the document column into one row per word + primary key

```sql
SELECT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
```

```sh
natural_language=# SELECT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
 id | keyword
----+----------
  1 | This
  1 | is
  1 | SQL
  1 | and
  1 | Python
  1 | and
  1 | other
  1 | fun
  1 | teaching
  1 | stuff
  2 | More
  2 | people
  2 | should
  2 | learn
  2 | SQL
  2 | from
  2 | UMSI
  3 | UMSI
  3 | also
  3 | teaches
  3 | Python
  3 | and
  3 | also
  3 | SQL
(24 rows)
```

### Breaking the document column into one row per word + primary key discarding duplicate rows

```sql
SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
```

```sh
natural_language=# SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
 id | keyword
----+----------
  1 | and
  1 | fun
  1 | is
  1 | other
  1 | Python
  1 | SQL
  1 | stuff
  1 | teaching
  1 | This
  2 | from
  2 | learn
  2 | More
  2 | people
  2 | should
  2 | SQL
  2 | UMSI
  3 | also
  3 | and
  3 | Python
  3 | SQL
  3 | teaches
  3 | UMSI
(22 rows)
```

### Insert the keyword and doc_id into the `docs_gin` table

```sql
INSERT INTO docs_gin (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
```

```sh
natural_language=# INSERT INTO docs_gin (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(D.doc, ' ')) AS s(keyword)
ORDER BY id;
INSERT 0 22
natural_language=# SELECT * FROM docs_gin;
 keyword  | doc_id
----------+--------
 and      |      1
 fun      |      1
 is       |      1
 other    |      1
 Python   |      1
 SQL      |      1
 stuff    |      1
 teaching |      1
 This     |      1
 from     |      2
 learn    |      2
 More     |      2
 people   |      2
 should   |      2
 SQL      |      2
 UMSI     |      2
 also     |      3
 and      |      3
 Python   |      3
 SQL      |      3
 teaches  |      3
 UMSI     |      3
(22 rows)
```

### Some queries we can run

#### Find all the distinct documents that match a keyword

```sql
SELECT DISTINCT doc FROM docs as D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = 'UMSI';
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs as D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = 'UMSI';
                  doc
----------------------------------------
 More people should learn SQL from UMSI
 UMSI also teaches Python and also SQL
(2 rows)
```

#### We can remove duplicates and have more than one keyword

```sql
SELECT DISTINCT id, doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword IN ('fun', 'people');
```

```sh
natural_language=# SELECT DISTINCT id, doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword IN ('fun', 'people');
 id |                         doc
----+-----------------------------------------------------
  1 | This is SQL and Python and other fun teaching stuff
  2 | More people should learn SQL from UMSI
(2 rows)
```

#### We can handle a query with a phrase as well

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array('I want to learn', ' '));
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array('I want to learn', ' '));
                  doc
----------------------------------------
 More people should learn SQL from UMSI
(1 row)
```

### This can go sideways if we include stop words like "the", "is", "and" etc

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array('Search for Lemons and Neons', ' '));
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array('Search for Lemons and Neons', ' '));
                         doc
-----------------------------------------------------
 UMSI also teaches Python and also SQL
 This is SQL and Python and other fun teaching stuff
(2 rows)
```

As you can see, the query is not very good, since it is matching on the stop words "and" and "for". This is a common problem with inverted indexes, and it is usually solved by removing stop words from the index.

This process simulated creating a `GIN` index on the `doc` column of the `docs` table, which will allow us to quickly search for documents containing specific keywords. In this custom implementation we can get all rows with specific word using `WHERE` keyword on the `keyword` column of the `docs_gin` table.

`docs_gin` table is purely a text based inverted index and not a language based inverted index. It does not handle stop words, stemming, lemmatization, or any other NLP techniques that are commonly used in language based inverted indexes. It is just a simple mapping from keywords to document IDs.
