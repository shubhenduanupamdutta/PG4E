# Notes on Building a Deno KV Model with Secondary Indexes

---

## Data Model Design in Deno KV

---

- Deno KV is a key-value store, so data modeling is different from relational databases

### Deno Keys are Arrays

- Keys are hierarchical logical keys represented as JavaScript arrays
- Example: `['books', 'Hamlet']` could be a key for a book
- No fixed schema, so you can store any JSON document as the value
- Example value: `{ title: 'Hamlet', author: 'Shakespeare', year: 1603 }`

---

## A Classic SQL Model

---

### Suppose data you want to store is

| Title                      | ISBN          | Language | Author            |
| -------------------------- | ------------- | -------- | ----------------- |
| Introduction to Networking | 9781511654944 | en       | Charles Severance |
| Introducción a las redes   | 9781523627516 | es       | Fernando Tardio   |
| Mindshift                  | 9781101982853 | en       | Barbara Oakley    |
| Python for Everybody       | 9781530051120 | en       | Charles Severance |
| Python per tutti           | 1730907164    | it       | Vittore Zen       |

### There will be three tables in a relational database

1. authors
   - id (primary key)
   - name
2. languages
   - id (primary key)
   - language_code
3. books
   - id (primary key)
   - title
   - isbn
   - author_id (foreign key to authors.id)
   - language_id (foreign key to languages.id)

### Comparison of SQL vs Deno KV Model

- Efficient / indexed SQL queries
  - Book by ISBN
  - All books in a language
  - All books by an author
  - With a secondary index, exact title matches would be fast too

- In Deno
  - No foreign keys
  - No primary keys
  - No secondary indexes

---

## Deno Secondary Indexes

---

- In Deno, for each query that we want to be efficient we use a different initial prefix
- Let's assume that ISBN is the truly unique key, and secondary keys can have duplicates
- We can create a "foreign logical key" by adding the unique logical key to all the secondary keys

```javascript
kv.set(["books", "isbn", "9781511654944"], {
	title: "Introduction to Networking",
	author: "Charles Severance",
	language: "en",
});
kv.set(["books", "title", "Introduction to Networking", "9781511654944"], {});
kv.set(["books", "author", "Charles Severance", "9781511654944"], {});
kv.set(["books", "language", "en", "9781511654944"], {});
```

- This way we can efficiently query by ISBN, title, author, or language
- This is a common pattern in NoSQL databases to achieve efficient queries without joins
- We need to add ISBN to every key because other fields can have duplicates, but ISBN is unique and can serve as a reference to the main record.
- We don't need to provide the value for the secondary index records, we can just use an empty object or null, since the logical key (here ISBN) we get can be queried to get the full record from the main key.

```javascript
kv.list[{ prefix: ["books", "author", "Charles Severance"] }];
```
