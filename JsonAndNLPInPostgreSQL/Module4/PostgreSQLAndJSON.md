# Notes on PostgreSQL and JSON

---

## JSON in PostgreSQL

---

- Postgres support for JSON has evolved over time.
- JSON presence in postgres is somewhat a reaction to JSON based NoSQL databases like MongoDB and CouchDB.

### JSON type in PostgreSQL

#### `HSTORE`

**HSTORE** is a column type that can store keys and values. It frankly looks like a column that is a PHP Array/ Python dictionary without the support for nested data structure.

**HSTORE** stores key value pairs efficiently and has good support for indexes to allow `WHERE` clauses to look inside the column efficiently. Indexes on HSTORE columns were easy to create and use.

#### `JSON` (From PostgreSQL 9.3)

**JSON** is best thought of as a pre-release of `JSONB`. A _JSON_ column was a glorified `TEXT` column with some really nifty built-in functions that kept application developers from "hacking up" their own JSON-like TEXT columns. Things like JSON operators and functions were nicely carried over into `JSONB`.

This **layer of functions and indexes** on top of a `TEXT` column is a strategy that has been used by relational databases to quickly build and release JSON support to counter the move to NoSQL databases.

#### `JSONB`

**JSONB** is a completely new column type that stores parsed JSON densely to save space, make indexing more effective, and make query/retrieval efficient. The "B" stands for "better", but I like to think of it as "binary", acknowledging that it is no longer a big TEXT column that happens to contain a JSON string.

In a sense, the `JSONB` support in PostgreSQL is a merger of the efficient storage and indexing of the `HSTORE` merged with rich operator and function support of `JSON`.

---

## JSONB Operators

---

### `->>` operator

```sql
SELECT (body ->> 'count')::int FROM jtrack WHERE body->>'name' = 'Summer Nights';
```

This query retrieves the value associated with the key 'count' from the JSONB column 'body' in the 'jtrack' table, where the value associated with the key 'name' is 'Summer Nights'. The `->>` operator is used to extract the value as text, and then it is cast to an integer using `::int`.

### `@>` operator

```sql
SELECT * FROM jtrack WHERE body @> '{"name": "Summer Nights"}';
```

This query retrieves all rows from the 'jtrack' table where the JSONB column 'body' contains a key-value pair with the key 'name' and the value 'Summer Nights'. The `@>` operator checks if the left JSONB value contains the right JSONB value.

### `#>>` operator: `json#>>text[] -> text`

```sql
-- Extracts JSON sub-object at the specified path as text.

'{"a": {"b": ["foo","bar"]}}'::json #>> '{a,b,1}' → bar
```

This query extracts the value at the specified path from the JSON object. In this case, it retrieves the second element of the array associated with the key 'b' within the nested object 'a', which is 'bar'. The `#>>` operator is used to extract a JSON sub-object as text based on a specified path.

### `#>` operator: `json#>text[] -> json`

```sql
Extracts JSON sub-object at the specified path, where path elements can be either field keys or array indexes.

'{"a": {"b": ["foo","bar"]}}'::json #> '{a,b,1}' → "bar"
```

This query extracts the value at the specified path from the JSON object, similar to the `#>>` operator, but it returns the result as a JSON value instead of text. In this case, it retrieves the second element of the array associated with the key 'b' within the nested object 'a', which is "bar". The `#>` operator is used to extract a JSON sub-object based on a specified path and return it as JSON.

### `?` operator: `json?text -> boolean`

```sql
-- Does the text string exist as a top-level key or array element within the JSON value?

'{"a":1, "b":2}'::jsonb ? 'b' → t

'["a", "b", "c"]'::jsonb ? 'b' → t
```

This query checks if the specified text string exists as a top-level key in a JSON object or as an element in a JSON array. In the first example, it checks if the key 'b' exists in the JSON object, which returns true (t). In the second example, it checks if the element 'b' exists in the JSON array, which also returns true (t). The `?` operator is used to check for the existence of a key or element in a JSON value.

---

## Indexes on JSONB

---

### B-tree Indexes

Example SQL

```sql
CREATE INDEX jtrack_btree ON jtrack USING BTREE ((body->>'name'));
```

### GIN Indexes

Example SQL

```sql
CREATE INDEX jtrack_gin ON jtrack USING GIN (body);
```

### GIN Indexes with JSONB Path Ops

GIN Indexes with JSONB Path Ops

Example SQL

```sql
CREATE INDEX jtrack_gin_path_ops ON jtrack USING GIN (body jsonb_path_ops);
```
