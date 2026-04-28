# Assignment 2: GIN `ts_vector` Index

In this assignment, you will create a table of documents and then produce a GIN-based ts_vector index on the documents.

---

## DROP the `docs03` table built in previous assignment

```sql
DROP TABLE IF EXISTS docs03;
```

---

## Create a `docs` table

```sql
CREATE TABLE docs03 (id SERIAL, doc TEXT, PRIMARY KEY(id));
```

---

## Create a ts_vector GIN index on the `doc` column

```sql
CREATE INDEX fulltext03 ON docs03 USING gin(to_tsvector('english', doc));
```

---

## Insert some data into the `docs03` table

```sql
INSERT INTO docs03 (doc) VALUES
('communicate with it Python is not intelligent You are'),
('really just having a conversation with yourself but using proper'),
('In a sense when you use a program written by someone else the'),
('conversation is between you and those other programmers with Python'),
('acting as an intermediary Python is a way for the creators of programs'),
('to express how the conversation is supposed to proceed And in just a'),
('few more chapters you will be one of those programmers using Python to'),
('talk to the users of your program'),
('Before we leave our first conversation with the Python interpreter you'),
('should probably know the proper way to say goodbye when interacting');
-- filler data
INSERT INTO docs03 (doc) SELECT 'Neon ' || generate_series(10000,200000);
```

---

## Query to run with explain analyze to see the index usage

```sql
EXPLAIN SELECT id, doc FROM docs03 WHERE to_tsquery('english', 'instructions') @@ to_tsvector('english', doc);
```
