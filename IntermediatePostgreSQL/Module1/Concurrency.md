# Notes on Concurrency in SQL

---

## Concurrency

---

- **Databases are designed to accept SQL commands from a variety of source simultaneously and make them _atomically_.**
- Database has to implement some order on any operations that include write operation or possible write operations because of maintaining data integrity and consistency.

---

## Transactions and Atomicity

---

- To implement atomicity, PostgreSQL "locks" areas before it starts and SQL command that might change an area of the database.
- All other access to that area must wait until area is unlocked.
- Something like a `Mutex` in programming languages.
- Better relational databases has better locking mechanism, so that it can allow more concurrency and less waiting.

### Single SQL statements are Atomic

- All the inserts statements are also atomic. Since if multiple inserts are there, and primary key needs to be generated for each row, so it needs to be locked until the insert is done. So if multiple inserts are there, they will be executed one after another, and not simultaneously. They need to be consecutive at least during primary key generation.

### Compound Statement

**There are statements which do more than one things in one statement for efficiency and concurrency.**
For example:

```sql
INSERT INTO fav (post_id, account_id, howmuch) VALUES (1, 1, 1) RETURNING *;  -- This is one atomic statement, but it does multiple things. It inserts a row and returns the inserted row.

UPDATE fav SET howmuch=howmuch+1 WHERE post_id=1 AND account_id=1 RETURNING *; -- This is also one atomic statement, but it does multiple things. It updates a row and returns the updated row.
```

### `ON CONFLICT` Clause

**This is a special clause that allows you to specify what to do when a conflict occurs during an insert operation.**

```sql
-- This will fail
INSERT INTO fav (post_id, account_id, howmuch) VALUES (1, 1, 1) RETURNING *; -- Since we have already inserted before
```

```sql
INSERT INTO fav (post_id, account_id, howmuch) VALUES (1, 1, 1)
  ON CONFLICT (post_id, account_id)
  DO UPDATE SET howmuch = fav.howmuch + 1
RETURNING *;
```

This will not fail, but it will update the existing row instead of inserting a new row, and it will return the updated row. This is also one atomic statement, but it does multiple things. It tries to insert a row, and if there is a conflict, it updates the existing row and returns the updated row. This is still one atomic statement.

---

## Multi-Statement Transactions

---

**Transactions are a sequence of SQL statements that are executed as a single unit of work. Either all the statements in the transaction are executed successfully, or none of them are executed.**

**`BEGIN;` - This is the command to start a transaction.**
**`COMMIT;` - This is the command to end a transaction and save all the changes made in the transaction.**
**`ROLLBACK;` - This is the command to end a transaction and undo all the changes made in the transaction.**

### Example 1: Rollback a Transaction

```sql
BEGIN;
SELECT howmuch FROM fav WHERE account_id=1 AND post_id=1 FOR UPDATE OF fave;
-- Time passes
UPDATE fav SET howmuch=999 WHERE account_id=1 AND post_id=1;
ROLLBACK;
SELECT howmuch FROM fav WHERE account_id=1 AND post_id=1;
```

In this example, we start a transaction with `BEGIN;`, then we select the `howmuch` value for a specific `account_id` and `post_id` with a `FOR UPDATE` clause, which locks the selected row for update. Then we simulate some time passing, and then we update the `howmuch` value to `999`. Finally, we roll back the transaction with `ROLLBACK;`, **which undoes all the changes made in the transaction.** When we select the `howmuch` value again, it will show the original value before the update, because the transaction was rolled back.

### Example 2: Commit a Transaction

```sql
BEGIN;
SELECT howmuch FROM fav WHERE account_id=1 AND post_id=1 FOR UPDATE OF fave;
-- Time passes
UPDATE fav SET howmuch=999 WHERE account_id=1 AND post_id=1;
COMMIT;
SELECT howmuch FROM fav WHERE account_id=1 AND post_id=1;
```

In this example, we start a transaction with `BEGIN;`, then we select the `howmuch` value for a specific `account_id` and `post_id` with a `FOR UPDATE` clause, which locks the selected row for update. Then we simulate some time passing, and then we update the `howmuch` value to `999`. Finally, we commit the transaction with `COMMIT;`, **which saves all the changes made in the transaction.** When we select the `howmuch` value again, it will show `999`, because the transaction was committed.

### Transaction Topics

#### Lock Strength

- `FOR UPDATE` - This is the strongest lock, it locks the selected rows for update, and no other transaction can access those rows until the lock is released.
- `NO KEY UPDATE` - This is a weaker lock, it allows other transactions to access the selected rows, but they cannot update the locked rows until the lock is released.

#### What to do when encountering a lock?

- `(WAIT)` - This is the default behavior, it will wait until the lock is released before proceeding with the transaction.
- `NOWAIT` - This will not wait, and it will return an error if the lock is not available.
- `SKIP LOCKED` - This will skip the locked rows and proceed with the transaction, it will not return an error if the lock is not available.
