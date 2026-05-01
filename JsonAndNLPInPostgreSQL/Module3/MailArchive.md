# Notes on Mail Archive Demonstration

---

## Basic Idea

---

Getting data from online resources, [Example Mailbox](http://mbox.dr-chuck.net/sakai.devel/4/6).
We will parse it using regex and load it into a PostgreSQL table.
We will create an inverse index which supports Natural Language Queries on the data.
We will then run some queries on the data to extract insights.

---

## Code Files

---

- [gmane.py](../python_and_postgres/gmane.py) - This file contains the code to parse the mailbox data and load it into a PostgreSQL table.
- [date_compatibility.py](../python_and_postgres/date_compatibility.py) - This file contains a helper function to parse the date from the mailbox data and convert it into a format that can be stored in PostgreSQL.
- [my_utils.py](../python_and_postgres/my_utils.py) - This file contains some helper functions to execute queries and handle errors.

You should run `gmane.py` to load the data into the PostgreSQL table. Before doing anything below.

---

## Create an Index on the body column

---

To create an index on the `body` column of the `messages` table, we can use the following SQL command:

```sql
CREATE INDEX messages_gin ON messages USING gin(to_tsvector('english', body));
```

```sh
python_postgres=# CREATE INDEX messages_gin ON messages USING gin(to_tsvector('english', body));
CREATE INDEX
python_postgres=# \d+ messages
                                                                Table "public.messages"
 Column  |           Type           | Collation | Nullable |               Default                | Storage  | Compression | Stats target | Description
---------+--------------------------+-----------+----------+--------------------------------------+----------+-------------+--------------+-------------
 id      | integer                  |           | not null | nextval('messages_id_seq'::regclass) | plain    |             |              |
 email   | text                     |           |          |                                      | extended |             |              |
 sent_at | timestamp with time zone |           |          |                                      | plain    |             |              |
 subject | text                     |           |          |                                      | extended |             |              |
 headers | text                     |           |          |                                      | extended |             |              |
 body    | text                     |           |          |                                      | extended |             |              |
Indexes:
    "messages_gin" gin (to_tsvector('english'::regconfig, body))
Access method: heap
```

---

## Let's run some queries on the data

---

### Let's check out the data index is being build upon

```sh
python_postgres=# SELECT to_tsvector('english', body) FROM messages LIMIT 1;
                                                                                                                                                                                                                                                                                                                                                                                                               to_tsvector
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 '/portal)':119 'architect':103 'austin':10,88 'automat':109 'better':17 'bof':7 'class':68 'collab':116 'collab.sakaiproject.org':118 'collab.sakaiproject.org/portal)':117 'confer':11 'cours':42 'develop':6,18,69,123 'discuss':13 'document':19,70 'email':57 'excel':5 'excit':52 'framework':102 'fun':93 'get':75 'ggolden@umich.edu':107 'glenn':97,98 'golden':100 'help':36,63 'ice':95 'idea':45 'interest':34 'll':74 'make':37 'mention':27 'messag':111 'michigan':106 'miss':91 'modifi':127 'much':51 'notif':110,131 'organ':78 'pleas':53 'prefer':135 'produc':14 'project':77 'pull':64 'r':99 'receiv':130 'recept':22 'sakai':72,101,115,122 'send':54 'sent':113 'site':124 'sorri':49 'storm':96 'thank':79 'today':2 'togeth':65 'univers':104 'will':61 'workspac':134 'world':67 'world-class':66 'would':32
(1 row)
```

### Using `to_tsquery` to check stemming

```sh
python_postgres=# SELECT to_tsquery('english', 'notification');
 to_tsquery
------------
 'notif'
(1 row)
```

### Is _neon_ in the body of first 10 messages?

```sh
python_postgres=# SELECT id, to_tsquery('english', 'neon') @@ to_tsvector('english', body) FROM messages LIMIT 10;
 id  | ?column?
-----+----------
   1 | f
   2 | f
   3 | f
   4 | f
   5 | f
 157 | f
   6 | f
   7 | f
   8 | f
   9 | f
(10 rows)
```

### Is _golden_ in the body of first 10 messages?

```sh
python_postgres=# SELECT id, to_tsquery('english', 'golden') @@ to_tsvector('english', body) FROM messages LIMIT 10;
 id  | ?column?
-----+----------
   1 | t
   2 | f
   3 | f
   4 | f
   5 | f
 157 | f
   6 | f
   7 | f
   8 | f
   9 | f
(10 rows)
```

---

## Alter column to add sender

---

To add a new column `sender` to the `messages` table, we can use the following SQL command:

```sql
ALTER TABLE messages ADD COLUMN sender TEXT;
```

And then add data to column using regex to extract the sender from the `headers` column.

```sql
UPDATE messages SET sender = substring(headers, '\nFrom: [^\n]*<([^>]*)');
```

```sh
python_postgres=# ALTER TABLE messages ADD COLUMN sender TEXT;
ALTER TABLE
python_postgres=# UPDATE messages SET sender = substring(headers, '\nFrom: [^\n]*<([^>]*)');
UPDATE 400
python_postgres=# SELECT sender FROM messages LIMIT 5;
           sender
----------------------------
 nuno@ufp.pt
 john.ellis@rsmart.com
 ggolden@umich.edu
 csev@umich.edu
 kevin.carpenter@rsmart.com
(5 rows)
```

---

## Let's run some queries again

---

### What is the subject and sender of messages that have _monday_ in the body?

```sh
python_postgres=# SELECT subject, sender FROM messages
python_postgres-# WHERE to_tsquery('english', 'monday') @@ to_tsvector('english', body) LIMIT 10;
                              subject                              |           sender
-------------------------------------------------------------------+----------------------------
 re: sakai 2.1 provider examples                                   | aaronz@vt.edu
 re: problems accessing the collab site with internet              | pgoldweic@northwestern.edu
 re: file picker for non-legacy tools                              | john.ellis@rsmart.com
 sakai 2.01 vt provider code                                       | aaronz@vt.edu
 re: problems accessing the collab site with internet explorer...  | aaronz@vt.edu
 re: regarding the section manager and other section related api's | jholtzman@berkeley.edu
 re: regarding the section manager and other section related api's | s-githens@northwestern.edu
 re: memory error with 2.1                                         | dgcotton@ucdavis.edu
 re: sectionmanager api's (nosuchbeandefinitionexception)          | jholtzman@berkeley.edu
 re: sectionmanager api's (nosuchbeandefinitionexception)          | esmiley@stanford.edu
(10 rows)
```

### Confirming that index is being used

```sh
python_postgres=# explain analyze SELECT subject, sender FROM messages
WHERE to_tsquery('english', 'monday') @@ to_tsvector('english', body) LIMIT 10;
                                                          QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=12.90..45.84 rows=10 width=56) (actual time=0.018..0.027 rows=10 loops=1)
   ->  Bitmap Heap Scan on messages  (cost=12.90..62.31 rows=15 width=56) (actual time=0.017..0.025 rows=10 loops=1)
         Recheck Cond: ('''monday'''::tsquery @@ to_tsvector('english'::regconfig, body))
         Heap Blocks: exact=6
         ->  Bitmap Index Scan on messages_gin  (cost=0.00..12.89 rows=15 width=0) (actual time=0.010..0.011 rows=15 loops=1)
               Index Cond: (to_tsvector('english'::regconfig, body) @@ '''monday'''::tsquery)
 Planning Time: 0.135 ms
 Execution Time: 0.044 ms
(8 rows)
```

PostgreSQL can support other languages but since we have not build `GIN` index on other languages, it will not be able to use the index for queries in other languages, it will use a sequential scan instead.

---

## Let's build a `GiST` index on the `body` column

---

To create a `GiST` index on the `body` column of the `messages` table, we can use the following SQL command:

```sql
DROP INDEX IF EXISTS messages_gin;
CREATE INDEX messages_gist ON messages USING gist(to_tsvector('english', body));
```

```sh
python_postgres=# DROP INDEX IF EXISTS messages_gin;
CREATE INDEX messages_gist ON messages USING gist(to_tsvector('english', body));
DROP INDEX
CREATE INDEX
```

`GiST` is smaller and easier to maintain and update.
