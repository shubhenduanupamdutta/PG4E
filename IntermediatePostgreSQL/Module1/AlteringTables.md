# Notes on Altering Tables

---

## `ALTER TABLE` Command

---

- You can change the schema, and SQL will convert the existing data to the new schema, all the while database is running.
- You have to take care that the application querying or changing data is not affected by schema change, otherwise it will blow up.
- This is needed in an evolving databases/applications. Or if you made a mistake.
- Following example shows how to drop a column. Second SQL command can be run immediately after, days, weeks or months later, it doesn't matter. It will work as long as the column exists.

```sql
CREATE TABLE fav (
    id SERIAL PRIMARY KEY,
    oops TEXT,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    UNIQUE (post_id, account_id)
);

ALTER TABLE fav DROP COLUMN oops;
```

- If nothing is using `oops` column, there will be no problem.
