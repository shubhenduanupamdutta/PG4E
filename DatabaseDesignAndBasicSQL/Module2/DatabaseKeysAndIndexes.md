# Notes on Database Keys and Indexes in PostgreSQL

---

## AUTO_INCREMENT

---

**Often as we make multiple tables and need to `JOIN` them together we need an integer primary key for each row so we can efficiently add a reference to a row in some other table as a foreign key.**

```sql
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL,
    name VARCHAR(128),
    email VARCHAR(128) UNIQUE,
    PRIMARY KEY (id)
);
```

- `SERIAL` is a special data type in PostgreSQL that automatically creates a sequence and assigns a unique integer value to the column for each new row inserted. It is commonly used for primary keys to ensure that each row has a unique identifier.
- `PRIMARY KEY` is a constraint that uniquely identifies each record in a table. It ensures that the values in the specified column(s) are unique and not null, which is essential for maintaining data integrity and enabling efficient querying and indexing.
- `UNIQUE` is a constraint that ensures all values in a column are different from each other. It allows for null values, but if a value is not null, it must be unique across the column. This is useful for columns like email addresses where duplicates are not allowed. This is a called `Logidcal Key` as it is not used for joining tables but is used to enforce uniqueness of values in a column. Postgres automatically creates an index on a column with a `UNIQUE` constraint to optimize queries that check for uniqueness.

---

## PostgreSQL Functions

---

**Many operations in PostgreSQL need to use built-in functions (like `NOW()` for dates).**

There are other functions like `CURRENT_DATE` and `CURRENT_TIMESTAMP` that can be used to get the current date and timestamp, respectively. These functions are often used in SQL queries to insert or update records with the current date and time, or to filter records based on date and time criteria. For example, you can use `CURRENT_DATE` to insert the current date into a table:

---

## Indexes

---

- As a table gets large (they always do), scanning all the data to find a single row becomes very costly.
- When `drchuck@gmail.com` logs into Twitter, they must find my password amongst 500 million users.
- There are techniques to greatly shorten the scan as long as you create data structures and maintain those structures - like shortcuts.
- Hashes or Tree are the most common.

### B-Tree Indexes

_A B-tree is a tree data structure that keeps data sorted and allows searches, sequential access, insertions, and deletions in logarithmic amortized time. The B-tree is optimized for systems that read and write large blocks of data. It is commonly used in databases and file systems._

- **B-Tree** - Balanced or Binary Tree
- They are good for exact look up, sorting and range look ups. And also for prefix lookups.

### Hashes

_A hash function is any algorithm or subroutine that maps large data sets to smaller data sets, called keys. For example, a single integer can serve as index to an array. The values returned by hash function are called hash values, hash codes, hash sums, checksums, or simply hashes. Hash functions are mostly used to accelerate table lookup or data comparison tasks such as finding items in a database._

Cool thing is hashing really reduces the numbers. Hashes are even quicker than B-trees for exact lookups. But they are not good for other types of lookups.

**Database decides for you which index to use based on datatype and query.**

---

## Summary

---

- SQL allows us to describe ths shape of data to be stored and give many hints to the database engine as to how we will be accessing or using the data.
- SQL is a language that provides us operations to Create, Read, Update and Delete (CRUD) data in a database.
