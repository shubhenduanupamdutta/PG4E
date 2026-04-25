# Notes on Using Regular Expressions in PostgreSQL

---

## Regular Expression for Parsing Columns

---

**Working in `em` table created already in `RegularExpressions.md`**

### Extracting the first number(s) from the email column

```sh
discuss=# SELECT substring(email FROM '[0-9]+') FROM em WHERE email ~ '[0-9]';
 substring
-----------
 79
 1
(2 rows)
```

### Extracting the domain from the email column

```sh
discuss=# SELECT substring(email FROM '.+@(.*)$') FROM em;
 substring
-----------
 umich.edu
 umich.edu
 uiuc.edu
 umuc.edu
 apple.com
 apple.com
(6 rows)
```

### Extracting the unique domains from the email column

```sh
discuss=# SELECT DISTINCT substring(email FROM '.+@(.*)$') FROM em;
 substring
-----------
 apple.com
 uiuc.edu
 umuc.edu
 umich.edu
(4 rows)
```

### Extracting the unique domains and their counts from the email column

```sh
discuss=# SELECT substring(email FROM '.+@(.*)$'),
count (substring(email FROM '.+@(.*)$'))
FROM em GROUP BY substring(email FROM '.+@(.*)$');
 substring | count
-----------+-------
 apple.com |     2
 uiuc.edu  |     1
 umuc.edu  |     1
 umich.edu |     2
(4 rows)
```

---

## Multiple Matches

---

- The `substring()` gets the first match in text column.
- We can get an array of matches using `regexp_matches()` function.

### Creating a table and inserting some data

```sql
CREATE TABLE tw (id SERIAL PRIMARY KEY, tweet TEXT);

INSERT INTO tw (tweet) VALUES
('This is #SQL and #FUN stuff'),
('More people should learn #SQL from #UMSI'),
('#UMSI also teaches #PYTHON');
```

```sh
discuss=# SELECT tweet FROM tw;
                  tweet
------------------------------------------
 This is #SQL and #FUN stuff
 More people should learn #SQL from #UMSI
 #UMSI also teaches #PYTHON
(3 rows)
```

### Extracting all the hashtags to SQL from the tweets

```sh
discuss=# SELECT id, tweet FROM tw WHERE tweet ~ '#SQL';
 id |                  tweet
----+------------------------------------------
  1 | This is #SQL and #FUN stuff
  2 | More people should learn #SQL from #UMSI
(2 rows)
```

### Extracting all the hashtags from the tweets

- `g` flag is used to get all the matches in the text column. It searches for all the matches in the text column and returns an array of matches.

```sh
discuss=# SELECT regexp_matches(tweet, '#([A-Za-z0-9_]+)', 'g') FROM tw;
 regexp_matches
----------------
 {SQL}
 {FUN}
 {SQL}
 {UMSI}
 {UMSI}
 {PYTHON}
(6 rows)
```

### Extracting the unique hashtags from the tweets

```sh
discuss=# SELECT DISTINCT regexp_matches(tweet, '#([A-Za-z0-9_]+)', 'g') FROM tw;
 regexp_matches
----------------
 {FUN}
 {UMSI}
 {SQL}
 {PYTHON}
(4 rows)
```

### Extracting the hashtags and row id from the tweets

```sh
discuss=# SELECT id, regexp_matches(tweet, '#([A-Za-z0-9_]+)', 'g') FROM tw;
id | regexp_matches
----+----------------
1 | {SQL}
1 | {FUN}
2 | {SQL}
2 | {UMSI}
3 | {UMSI}
3 | {PYTHON}
(6 rows)

```
