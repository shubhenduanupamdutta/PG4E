# Notes on Dates

---

## Date Types

---

**Dates are very important for databases.**

- `DATE` - **YYYY-MM-DD** format, no time component.
- `TIME` - **HH:MM:SS** format, no date component.
- `TIMESTAMP` - **YYYY-MM-DD HH:MM:SS** format, includes both date and time.
- `TIMESTAMPTZ` - Same as `TIMESTAMP` but with time zone information.
- Built-in PostgreSQL function `NOW()`. This has time zone information, so it returns `TIMESTAMPTZ` type.

---

## Setting Default Values

---

- We can save some code by auto-populating date fields when a row is INSERTed
- We will auto-set on UPDATEs later...

```sql
CREATE TABLE fav (
    id SERIAL PRIMARY KEY,
    oops TEXT, -- Will remove later with ALTER TABLE
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (post_id, account_id)
);
```

`created_at` and `updated_at` will be auto-populated with the current date and time when a new row is inserted, if no value is provided for those columns.

---

## `TIMESTAMPTZ` - Best Practice

---

- Store time stamps with timezone
- Prefer UTC for stored time stamps
- Convert to local time zone when retrieving

`pg_timezone_names` - view to see all time zones supported by PostgreSQL. You can use any of these time zones when inserting or retrieving data.
You can get all time zones with the following query:

```sql
select * FROM pg_timezone_names;
```

---

## Casting to different types

---

- We use the phrase _casting_ to mean convert from one type to another.
- Postgres has several forms of casting

```sh
pg4e=# SELECT NOW()::DATE, CAST(NOW() AS DATE), CAST(NOW() AS TIME);
    now     |    now     |       now
------------+------------+-----------------
 2026-04-20 | 2026-04-20 | 12:39:52.451763
(1 row)
```

- `NOW()::DATE` - This is the most common form of casting, using `::` operator.
- `CAST(NOW() AS DATE)` - This is the standard SQL form of casting, using the `CAST` function.
- `CAST(NOW() AS TIME)` - This is another example of using the `CAST` function to cast to a different type.

---

## Intervals

---

**We can do date interval arithmetic in PostgreSQL.**

```sh
pg4e=# SELECT NOW(), NOW() - INTERVAL '2 days', (NOW() - INTERVAL '2 days')::DATE;
              now              |           ?column?            |    date
-------------------------------+-------------------------------+------------
 2026-04-20 12:41:41.815575+00 | 2026-04-18 12:41:41.815575+00 | 2026-04-18
(1 row)
```

- `INTERVAL '2 days'` - This creates an interval of 2 days.
- `NOW() - INTERVAL '2 days'` - This subtracts 2 days from the current date and time.
- `(NOW() - INTERVAL '2 days')::DATE` - This casts the result to a `DATE` type, removing the time component.

### Some other `INTERVAL` examples

```sql
SELECT NOW() + INTERVAL '3 hours'; -- Adds 3 hours to the current time
SELECT NOW() - INTERVAL '1 month'; -- Subtracts 1 month from the current time
SELECT NOW() + INTERVAL '1 year 2 months'; -- Adds 1 year and 2 months to the current time
SELECT NOW() - INTERVAL '5 minutes'; -- Subtracts 5 minutes from the current time
```

---

## Using `date_trunc()`

---

**Sometimes we want to discard some of the accuracy that is in a timestamp.**

- `DATE_TRUNC()` - This function truncates a timestamp to a specified precision. This takes two arguments: the first is the precision to truncate to (e.g., 'day', 'hour', 'minute'), and the second is the timestamp to truncate.
- For example, `DATE_TRUNC('day', NOW())` will return the current date with the time set to 00:00:00, effectively giving you just the date part of the timestamp.

```sh
pg4e=# SELECT NOW(), DATE_TRUNC('day', NOW()), DATE_TRUNC('hour', NOW());
              now              |       date_trunc       |       date_trunc
-------------------------------+------------------------+------------------------
 2026-04-20 12:45:25.711188+00 | 2026-04-20 00:00:00+00 | 2026-04-20 12:00:00+00
(1 row)
```

---

## Performance: Table Scans

---

**Not all equivalent queries have the same performance. Some queries may require a full table scan, while others can take advantage of indexes, due to the way the query is written or the types of operations being performed.**

- Following is a slow query, by using casting

```sql
SELECT id, content, created_at FROM comment
  WHERE created_at::DATE = NOW()::DATE;
```

- Following is a fast query, by using `DATE_TRUNC()`

```sql
SELECT id, content, created_at FROM comment
  WHERE created_at >= DATE_TRUNC('day', NOW())
  AND created_at < DATE_TRUNC('day', NOW() + INTERVAL '1 day');
```

- The first query is slow because it casts `created_at` to `DATE`, which prevents the use of any index on `created_at`, resulting in a full table scan.
- The second query is fast because it uses a range condition on `created_at`, which can take advantage of an index on `created_at`, resulting in a much faster query.
