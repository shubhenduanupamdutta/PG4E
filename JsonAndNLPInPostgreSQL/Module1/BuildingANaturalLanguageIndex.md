# Notes on Building a Natural Language Index in PostgreSQL

---

## Building a Natural Language Index Manually using SQL

---

### Techniques for Building a Natural Language Index

#### Removing Stop Words

**Some words like "and", "for", "the" are very common in English and they do not add much meaning to the text. These words are called _stop words_. Normal text based inverted indexes will include these stop words, which can lead to a lot of noise in the search results.**

#### Case Normalization

**Another point is lowercase and uppercase versions of the same word are treated as different words in a normal text based inverted index. This can also lead to missing out on relevant search results. Since their meaning is the same, we want to treat them as the same word in the index.**

#### Stemming

**You have lot of words which are variations of the same word, for example "run", "running", "ran" are all variations of the same word "run". A normal text based inverted index will treat these as different words, which can lead to missing out on relevant search results. Stemming is the process of reducing words to their root form, so that different variations of the same word are treated as the same word in the index.**

### Natural Language Indexes in PostgreSQL

```sh
natural_language=# SELECT cfgname FROM pg_ts_config;
  cfgname
------------
 simple
 arabic
 armenian
 basque
 catalan
 danish
 dutch
 english
 finnish
 french
 german
 greek
 hindi
 hungarian
 indonesian
 irish
 italian
 lithuanian
 nepali
 norwegian
 portuguese
 romanian
 russian
 serbian
 spanish
 swedish
 tamil
 turkish
 yiddish
(29 rows)
```

### Manual Building

Data is already in the `docs` table.

```sh
natural_language=# SELECT * FROM docs;
 id |                         doc
----+-----------------------------------------------------
  1 | This is SQL and Python and other fun teaching stuff
  2 | More people should learn SQL from UMSI
  3 | UMSI also teaches Python and also SQL
(3 rows)
```

### Create `docs_gin` table

```sql
natural_language=# CREATE TABLE docs_gin (keyword TEXT, doc_id INTEGER REFERENCES docs(id) ON DELETE CASCADE);
CREATE TABLE
natural_language=# \d+ docs_gin;
                                         Table "public.docs_gin"
 Column  |  Type   | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
---------+---------+-----------+----------+---------+----------+-------------+--------------+-------------
 keyword | text    |           |          |         | extended |             |              |
 doc_id  | integer |           |          |         | plain    |             |              |
Foreign-key constraints:
    "docs_gin_doc_id_fkey" FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
Access method: heap
```

### Crate a `stop_words` table and insert some stop words into it

```sh
natural_language=# CREATE TABLE stop_words (word TEXT UNIQUE);
CREATE TABLE
natural_language=# INSERT INTO stop_words (word) VALUES ('is'), ('this'), ('and');
INSERT 0 3
natural_language=# SELECT * FROM stop_words;
 word
------
 is
 this
 and
(3 rows)
```

### Insert data from `docs` table into `docs_gin` table

- We will lowercase the keywords to handle case normalization.
- We will use `DISTINCT` to remove duplicate keywords for the same document.

```sql
INSERT INTO docs_gin (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) AS s(keyword)
WHERE s.keyword NOT IN (SELECT word FROM stop_words)
ORDER BY id;
```

```sh
natural_language=# INSERT INTO docs_gin (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) AS s(keyword)
WHERE s.keyword NOT IN (SELECT word FROM stop_words)
ORDER BY id;
INSERT 0 18
natural_language=# SELECT * FROM docs_gin;
 keyword  | doc_id
----------+--------
 fun      |      1
 other    |      1
 python   |      1
 sql      |      1
 stuff    |      1
 teaching |      1
 from     |      2
 learn    |      2
 more     |      2
 people   |      2
 should   |      2
 sql      |      2
 umsi     |      2
 also     |      3
 python   |      3
 sql      |      3
 teaches  |      3
 umsi     |      3
(18 rows)
```

### Some queries we can run now

#### A one word query

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = lower('UMSI');
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = lower('UMSI');
                  doc
----------------------------------------
 More people should learn SQL from UMSI
 UMSI also teaches Python and also SQL
(2 rows)
```

#### A Multi word query

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array(lower('Meet fun people'), ' '));
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = ANY(string_to_array(lower('Meet fun people'), ' '));
                         doc
-----------------------------------------------------
 More people should learn SQL from UMSI
 This is SQL and Python and other fun teaching stuff
(2 rows)
```

#### A stop word query

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = lower('and');
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = lower('and');
 doc
-----
(0 rows)
```

### Now let's add `stemming` to our index

#### Create a "dictionary" of word -> stem

```sql
CREATE TABLE docs_stem (word TEXT, stem TEXT);
INSERT INTO docs_stem (word, stem) VALUES
('teaching', 'teach'), ('teaches', 'teach');
```

```sh
natural_language=# CREATE TABLE docs_stem (word TEXT, stem TEXT);
INSERT INTO docs_stem (word, stem) VALUES
('teaching', 'teach'), ('teaches', 'teach');
CREATE TABLE
INSERT 0 2
natural_language=# SELECT * FROM docs_stem;
   word   | stem
----------+-------
 teaching | teach
 teaches  | teach
(2 rows)
```

#### Let's update our query for inserting data into `docs_gin` table to handle stemming as well

##### Move the initial word extraction into a sub-query

```sql
SELECT id, keyword FROM (
    SELECT DISTINCT id, s.keyword AS keyword
    FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
) AS X;
```

##### Add the stems as third column (may or may not exist)

```sql
SELECT id, keyword, stem FROM (
    SELECT DISTINCT id, s.keyword AS keyword
    FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
) AS K
LEFT JOIN docs_stem AS S ON K.keyword = S.word;
```

##### If the stem is there, use it

```sql
SELECT id,
CASE
    WHEN stem IS NOT NULL THEN stem
    ELSE keyword
END AS awesome,
keyword, stem
FROM (
    SELECT DISTINCT id, lower(s.keyword) AS keyword
    FROM docs AS D, unnest(string_to_array(D.doc, ' ')) s(keyword)
) AS K
LEFT JOIN docs_stem AS S ON K.keyword = S.word;
```

##### Using null-coalescing operator

**Null Coalescing** - return the first non-null in a list

```sql
SELECT COALESCE(NULL, NULL, 'umsi'); -- returns 'umsi'
SELECT COALESCE(NULL, 'sql', 'umsi'); -- returns 'sql'
SELECT COALESCE('umsi', NULL, 'SQL'); -- returns 'umsi'
```

Using `COALESCE` to simplify the query

```sql
SELECT id, COALESCE(stem, keyword) AS keyword
FROM (
    SELECT DISTINCT id, s.keyword AS keyword
    FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
) AS K
LEFT JOIN docs_stem AS S ON K.keyword = S.word;
```

##### Insert only `stems` and without stop words

```sql
INSERT INTO docs_gin (doc_id, keyword)
SELECT id, COALESCE(stem, keyword) AS keyword
FROM (
    SELECT DISTINCT id, s.keyword AS keyword
    FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
    WHERE s.keyword NOT IN (SELECT word FROM stop_words)
) AS K
LEFT JOIN docs_stem AS S ON K.keyword = S.word;
```

```sh
natural_language=# INSERT INTO docs_gin (doc_id, keyword)
SELECT id, COALESCE(stem, keyword) AS keyword
FROM (
    SELECT DISTINCT id, s.keyword AS keyword
    FROM docs AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
    WHERE s.keyword NOT IN (SELECT word FROM stop_words)
) AS K
LEFT JOIN docs_stem AS S ON K.keyword = S.word
natural_language-# ;
INSERT 0 18
natural_language=# SELECT * FROM docs_gin;
 keyword | doc_id
---------+--------
 also    |      3
 from    |      2
 fun     |      1
 learn   |      2
 more    |      2
 other   |      1
 people  |      2
 python  |      3
 python  |      1
 should  |      2
 sql     |      2
 sql     |      1
 sql     |      3
 stuff   |      1
 teach   |      3
 teach   |      1
 umsi    |      3
 umsi    |      2
(18 rows)
```

### Let's do some queries after adding stemming

#### A one word query with no stem

```sql
SELECT COALESCE((SELECT stem FROM docs_stem WHERE word=lower('SQL')), lower('SQL'));
```

```sh
natural_language=# SELECT COALESCE((SELECT stem FROM docs_stem WHERE word=lower('SQL')), lower('SQL'));
 coalesce
----------
 sql
(1 row)
```

#### Handling the stems in queries. Use the keyword if there is no stem

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = COALESCE((SELECT stem FROM docs_stem WHERE word=lower('teaches')), lower('teaches'));
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = COALESCE((SELECT stem FROM docs_stem WHERE word=lower('teaches')), lower('teaches'));
                         doc
-----------------------------------------------------
 This is SQL and Python and other fun teaching stuff
 UMSI also teaches Python and also SQL
(2 rows)
```

#### Prefer the stem over the actual keyword

```sql
SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = COALESCE((SELECT stem FROM docs_stem WHERE word=lower('teaches')), lower('teaches'));
```

```sh
natural_language=# SELECT DISTINCT doc FROM docs AS D
JOIN docs_gin AS G ON D.id = G.doc_id
WHERE G.keyword = COALESCE((SELECT stem FROM docs_stem WHERE word=lower('teaches')), lower('teaches'));
                         doc
-----------------------------------------------------
 This is SQL and Python and other fun teaching stuff
 UMSI also teaches Python and also SQL
(2 rows)
```

## Conflation: The process of treating different forms of a word as the same word in an index is called _conflation_. Stemming is one technique for conflation, but there are other techniques as well, such as lemmatization, which is a more sophisticated technique that takes into account the context of the word to determine its root form
