# Notes on Working with Tables and PostgreSQL

---

## SQL: Basic Commands

---

### SQL: Insert

**The `INSERT` statement inserts a row into a table.**

```sql
INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');
```

Above is an example of how to insert a new user into the `users` table with the name "John Doe" and email `john.doe@example.com`.

You specify fields (columns) to insert into in first parentheses, followed by the `VALUES` keyword and the corresponding values in the second parentheses. There is 1:1 correspondence between the fields and values.

### SQL: Delete

**Deletes a row in table based on a selection criteria if provided. Otherwise deletes all rows.**

```sql
DELETE FROM users WHERE email='ted@umich.edu';
```

The above command deletes the user with email `ted@umich.edu` from the `users` table. If the `WHERE` clause is omitted, all rows in the `users` table would be deleted.

**WHERE** clause is used to specify the condition for deletion. It is important to use it carefully to avoid unintentional data loss.

SQL is not a procedural language. ​And so there is no real concept of a loop in SQL. ​The DELETE FROM implies loop. ​And if you don't say WHERE, ​if you take this off, ​it would be like delete all the rows

This essentially makes, if you provide `WHERE` clause, an if statement for check. Mind you this is not how database works internally, but this is how we can think about it. ​If you don't provide `WHERE` clause, then it is like a loop that goes through all the rows and deletes them.

It essentially goes directly to the row where email is `ted@umich.edu` and deletes it. ​It doesn't have to loop through all the rows to find it. ​It can directly go to that row and delete it. ​This is because of the way databases are designed, they have indexes that allow them to quickly find rows based on certain criteria.

### SQL: Update

**Allows the updating of a field with a `WHERE` clause.**

```sql
UPDATE users SET name='Charles' WHERE email='csev@umich.edu';
```

The above command updates the name of the user with email `csev@umich.edu` to "Charles".
The `UPDATE` statement is used to modify existing records in a table. The `SET` clause specifies the column to be updated and the new value. The `WHERE` clause is used to specify which record(s) should be updated. If the `WHERE` clause is omitted, all records in the table will be updated with the new value.
Again here `UPDATE` implies a loop. But again this is just a way of thinking about it. ​It is not how the database works internally.

It updates every row where the `WHERE` clause is true.

### SQL: Select

**Retrieves a group of records - you can either retrieve all the records or a subset of the records with a `WHERE` clause.**

```sql
SELECT * FROM users;
```

The above command retrieves all records from the `users` table. The `*` is a wildcard that means "all columns". You can also specify specific columns instead of using `*`.

```sql
SELECT name, email FROM users;
```

The above command retrieves only the `name` and `email` columns from the `users` table.

```sql
SELECT * FROM users WHERE email='csev@umich.edu';
```

The above command retrieves all columns for the user with email `csev@umich.edu` from the `users` table. The `WHERE` clause is used to filter the results based on a specific condition.

#### Select: Sorting with `ORDER BY`

**You can add an `ORDER BY` clause to `SELECT` statements to get results sorted in ascending or descending order.**

```sql
SELECT * FROM users ORDER BY email
```

The above command retrieves all records from the `users` table and sorts them in ascending order based on the `email` column.
That means the results will be sorted alphabetically by email, from A to Z.

```sql
SELECT * FROM users ORDER BY email DESC;
```

The above command retrieves all records from the `users` table and sorts them in descending order based on the `email` column.
That means the results will be sorted alphabetically by email, from Z to A.

### The `LIKE` clause

**We can do wildcard matching in a `WHERE` clause using the `LIKE` operator.**

```sql
SELECT * FROM users WHERE email LIKE '%e%';
```

The above command retrieves all records from the `users` table where the `email` column contains the letter "e". The `%` is a wildcard that matches any sequence of characters, so `%e%` means "any string that contains 'e'".

This will commonly (unless configured specifically) will start a full scan.

### The `LIMIT/OFFSET` clause

- \*\*We can request the first "n" rows, or the first "n" rows after skipping some rows.
- The `WHERE` and `ORDER BY` clauses happen **before** the `LIMIT` and `OFFSET` clauses.\*\*
- THE `OFFSET` starts from row 0.

```sql
SELECT * FROM users ORDER BY email DESC LIMIT 2;
```

This command retrieves the first 2 records from the `users` table sorted in descending order by the `email` column.

```sql
SELECT * FROM users ORDER BY email OFFSET 1 LIMIT 2;
```

This command retrieves 2 records from the `users` table sorted in ascending order by the `email` column, starting from the second record (skipping the first record).

### Counting Rows with `COUNT`

**You can request to receive the _count_ of the rows that would be retrieved instead of rows.**

```sql
SELECT COUNT(*) FROM users;
```

The above command retrieves the total number of records in the `users` table. The `COUNT(*)` function counts all rows in the table.

```sql
SELECT COUNT(*) FROM users WHERE email='csev@umich.edu';
```

---

## This is not too exciting (so far)

- Tables pretty much look like big, fast programmable spreadsheets with rows, columns and commands.
- The power comes when we have more than one table and we can exploit the relationships between the tables.
