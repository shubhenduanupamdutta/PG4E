# Notes on Subqueries

---

## What is a Subquery?

---

**A query within a query.**
_Can use a value or set of values in a query that are computed by another query._

### Suppose we want to know what is the comment in a comment table where email is some value. But you have account and command tables

### Using Two Queries

1. First query to get the `id` from the `account` table where `email` is 'ed@umich.edu'

   ```sql
   SELECT id FROM account WHERE email='ed@umich.edu';
   ```

   Suppose it returns `7` as id.

2. Then use the result of the first query to get the comment from the `comment` table

   ```sql
   SELECT content FROM comment WHERE account_id = 7;
   ```

### Using a Subquery

```sql
SELECT content FROM comment
  WHERE account_id = (SELECT id FROM account WHERE email='ed@umich.edu');
```

---

## Why subqueries are not recommended?

---

**Subqueries are less performant. So if application is performance sensitive that don't use subqueries. But sometimes performance is not a concern, like Data Mining, and subqueries can be more readable.**

### Why subqueries are less performant?

- In a subquery we are explicitly telling database to how to do it. So database can only optimize two queries partially.
- Database doesn't have full freedom to optimize the query.
- It stops optimization analysis at the subquery boundary. So it can't optimize the whole query as a single unit, which can lead to less efficient execution plans.
- There is also a temporary table created to hold the results of the subquery, which can add overhead and slow down the query execution.

### Using subquery instead of using `HAVING` clause

#### Original query using `HAVING` clause

Following is more performant query, by using `HAVING` clause
This also has more chance of being optimized by database and Database Administrator.

```sql
SELECT COUNT(abbrev) as ct, abbrev FROM pg_timezone_names
WHERE is_dst='t' GROUP BY abbrev HAVING COUNT(abbrev) > 10;
```

#### Rewritten query using a subquery

```sql
SELECT ct, abbrev FROM (
    SELECT COUNT(abbrev) as ct, abbrev FROM pg_timezone_names
    WHERE is_dst='t' GROUP BY abbrev
) AS subquery WHERE ct > 10;
```
