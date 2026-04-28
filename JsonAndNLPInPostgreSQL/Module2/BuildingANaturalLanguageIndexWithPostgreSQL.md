# Notes on Building a Natural Language Index with PostgreSQL

---

## Text Search Functions and Operators

---

**PostgreSQL provides some functions that turn a text document/string into an "array" with stemming, stop words and other language-oriented features.**

### `to_tsvector()` - Returns a list of words that represent the document, with stemming and stop words removed

- This function takes two arguments: the first is the language (e.g., 'english'), and the second is the text document/string to be processed.
- It returns a `tsvector` which is a sorted list of distinct lexemes (words) that are normalized to their root form (stemming) and have stop words removed.
- `tsvector` also keep track of ordering of the words in the document, which can be useful for phrase searching and ranking results.

#### NOTE: It is called a vector because the words are mapped to a n-dimensional vector space, where each dimension corresponds to a unique word in the document collection. The presence of a word in a document is represented by a non-zero value in the corresponding dimension of the vector

```sh
natural_language=# SELECT to_tsvector('english', 'UMSI also teaches Python and also SQL');
                   to_tsvector
--------------------------------------------------
 'also':2,6 'python':4 'sql':7 'teach':3 'umsi':1
(1 row)
```

### `to_tsquery()` returns a list of words with operators to representations various logical combinations of words

- This function also takes two arguments: the first is the language (e.g., 'english'), and the second is the query string to be processed.
- It returns a `tsquery` which is a representation of the query string that can be used to search against a `tsvector`.
- Most common used operators are for matching: `tsquery @@ tsvector`

```sh
natural_language=# SELECT to_tsquery('english', 'teaching') @@ to_tsvector('english', 'UMSI also teaches Python and also SQL');
 ?column?
----------
 t
(1 row)
```

- `@@` is the text search match operator, which returns true if the `to_tsvector` matches the `to_tsquery`.

---

## Creating a Natural Language Index

---

### Creating a `docs` table

```sql
CREATE TABLE docs (
    id SERIAL PRIMARY KEY,
    doc TEXT
);
```

Data in `docs` table

```sh
natural_language=# SELECT * FROM docs ORDER BY id LIMIT 3;
 id |                         doc
----+-----------------------------------------------------
  1 | This is SQL and Python and other fun teaching stuff
  2 | More people should learn SQL from UMSI
  3 | UMSI also teaches Python and also SQL
(3 rows)
natural_language=# SELECT count(*) FROM docs;
 count
--------
 100003
(1 row)
```

### Create a Natural Language Index

```sql
CREATE INDEX gin1 ON docs USING gin(to_tsvector('english', doc));
```

```sh
natural_language=# CREATE INDEX gin1 ON docs USING gin(to_tsvector('english', doc));
CREATE INDEX
natural_language=# \d+ docs;
                                                       Table "public.docs"
 Column |  Type   | Collation | Nullable |             Default              | Storage  | Compression | Stats target | Description
--------+---------+-----------+----------+----------------------------------+----------+-------------+--------------+-------------
 id     | integer |           | not null | nextval('docs_id_seq'::regclass) | plain    |             |              |
 doc    | text    |           |          |                                  | extended |             |              |
Indexes:
    "docs_pkey" PRIMARY KEY, btree (id)
    "gin1" gin (to_tsvector('english'::regconfig, doc))
Referenced by:
    TABLE "docs_gin" CONSTRAINT "docs_gin_doc_id_fkey" FOREIGN KEY (doc_id) REFERENCES docs(id) ON DELETE CASCADE
Access method: heap
```

### Let's query the table

```sql
SELECT id, doc FROM docs
WHERE to_tsquery('english', 'learn') @@ to_tsvector('english', doc);
```

```sh
natural_language=# SELECT id, doc FROM docs
WHERE to_tsquery('english', 'learn') @@ to_tsvector('english', doc);
 id |                  doc
----+----------------------------------------
  2 | More people should learn SQL from UMSI
(1 row)
```

### Explain Analysis of the query

```sh
natural_language=# explain analyze SELECT id, doc FROM docs
WHERE to_tsquery('english', 'learn') @@ to_tsvector('english', doc);
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on docs  (cost=19.71..906.22 rows=500 width=34) (actual time=0.015..0.016 rows=1 loops=1)
   Recheck Cond: ('''learn'''::tsquery @@ to_tsvector('english'::regconfig, doc))
   Heap Blocks: exact=1
   ->  Bitmap Index Scan on gin1  (cost=0.00..19.59 rows=500 width=0) (actual time=0.011..0.011 rows=1 loops=1)
         Index Cond: (to_tsvector('english'::regconfig, doc) @@ '''learn'''::tsquery)
 Planning Time: 0.091 ms
 Execution Time: 0.031 ms
(7 rows)
```

---

## Some other functions and operators

---

### `plainto_tsquery()` - Converts a plain text query into a `tsquery`

This implies **and** between the words obtained.

```sh
natural_language=# SELECT plainto_tsquery('english', 'SQL Python');
 plainto_tsquery
------------------
 'sql' & 'python'
(1 row)

natural_language=# SELECT plainto_tsquery('english', 'Teach teaches teaching and the if');
       plainto_tsquery
-----------------------------
 'teach' & 'teach' & 'teach'
(1 row)
```

### `phraseto_tsquery()` - Converts a plain text query into a `tsquery` with phrase searching

This implies **phrase searching** between the words obtained. Phrase searching means that the words must appear in the same order as they appear in the query string, and they must be adjacent to each other in the document.

```sh
natural_language=# SELECT phraseto_tsquery('english', 'SQL Python');
  phraseto_tsquery
--------------------
 'sql' <-> 'python'
(1 row)
```

### `websearch_to_tsquery()` - Converts a web search query into a `tsquery`

This function is designed to handle more complex queries that might include operators like `-` for negation, `|` for OR, and `&` for AND. It also handles phrase searching with double quotes.

```sh
natural_language=# SELECT websearch_to_tsquery('english', 'SQL -not Python');
 websearch_to_tsquery
----------------------
 'sql' & 'python'
(1 row)
```
