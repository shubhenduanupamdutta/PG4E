# Assignment 1: String Array GIN Index

---

## Create a `docs03` table

```sql
CREATE TABLE docs03 (id SERIAL, doc TEXT, PRIMARY KEY(id));
```

---

## Create a GIN index on the `doc` column

This is a text based index not a natural language index. It will not do stemming or remove stop words.

```sql
CREATE INDEX array03 ON docs03 USING gin (string_to_array(lower(doc), ' ') array_ops);
```

---

## Insert some data into the `docs03` table

### Inserting data into the `docs03` table

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
```

### Inserting some filler data into the `docs03` table

```sql
INSERT INTO docs03 (doc) SELECT 'Neon ' || generate_series(10000,20000);
```

---

## Query to run with explain analyze to see the index usage

```sql
EXPLAIN SELECT id, doc FROM docs03 WHERE '{conversation}' <@ string_to_array(lower(doc), ' ');
```

I needed to add more data to the table to see index being used.

```sql
INSERT INTO docs03 (doc) SELECT 'Neon ' || generate_series(20000,200000);
```
