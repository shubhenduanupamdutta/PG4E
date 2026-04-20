# Notes Stored Procedures

---

**Stored procedures are a set of SQL statements that can be stored in the database and executed as a single unit. They can be used to encapsulate complex logic, improve performance, and enhance security.**
This is also one of the things, on which people have strong opinions. Dr. Chuck also has strong opinion on this. He tends to avoid stored procedures at all costs because he tends to move from one database to another. Stored procedures are not portable at all.

But if you are a fixed flavor of relational database, and you are not going to change it, then stored procedures can be very useful. They can help you to improve performance and security.

---

## Stored Procedures in PostgreSQL

---

- A stored procedure is a bit of reusable code that runs inside of the database server.
- Technically there are multiple language choice but just use **plpgsql** which is a procedural language that is built into PostgreSQL.
- Generally quite non-portable.
- Usually the goal is to have fewer SQL statements.
- You should have a strong reason to use a stored procedure
  - Major performance problem
  - Harder to test/modify
  - No database portability
  - Some rule that **must** be informed.

### Example of a Stored Procedure

#### Recall

```sql
CREATE TABLE fav (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (post_id, account_id)
);

UPDATE fav SET howmuch=howmuch+1 WHERE post_id=1 AND account_id=1;

UPDATE fav SET howmuch=howmuch+1, updated_at=NOW() WHERE post_id=1 AND account_id=1;
```

#### Stored Procedure: Using a trigger for `updated_at` column

```sql
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON fav
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

UPDATE fav SET howmuch=howmuch+1 WHERE post_id=1 AND account_id=1;
```

In the above example, we created a stored procedure `trigger_set_timestamp` that sets the `updated_at` column to the current timestamp whenever a row in the `fav` table is updated. We then created a trigger `set_timestamp` that calls this stored procedure before any update on the `fav` table. This way, we don't have to manually update the `updated_at` column every time we update a row in the `fav` table.
