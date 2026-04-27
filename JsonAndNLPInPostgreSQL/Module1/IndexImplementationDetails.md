# Notes on Index Implementation Details in PostgreSQL

---

## How Index works?

---

Assume each row in the **users** table is about 1K, we could save a lot of time if somehow we had a hint about which row was in which block. This is where indexes come in.

- An index is a data structure that allows us to quickly locate rows in a table based on the values of one or more columns.
- Index stores in a sorted order the values of the indexed column(s) along with pointers to blocks where the corresponding rows are stored.
- We store the index data in 8K blocks as well.
- As index grow in size we need to avoid reading the entire index to look up one key. We need an index of an index. This is where B-trees come in.
- B-Trees keep the keys in sorted order by reorganizing the tree as keys are inserted and deleted. This allows us to quickly find the block that contains the key we are looking for, without having to read the entire index.

---

## PostgreSQL Index Types

---

### Forward Indexes

**You give the index a logical key and it tells you where to find the row that contains the key.** This metaphor is not perfect, since B-Tree indexes can give you a list of rows when doing prefix search.

- `B-Tree Indexes`: The default index type in PostgreSQL, used for most data types. They are balanced tree structures that allow for efficient searching, insertion, and deletion of keys.
- `BRIN - Block Range Indexes`: Smaller / faster if data is almost sorted. Size of BRIN is super tiny.
- `Hash Indexes`: Used for equality comparisons, but not as commonly used as B-trees. Quick lookup of long key strings.

### Inverted Indexes

**You give the index a string (query) and index gives you a list of _all_ the rows that match the query.** The most typical use case for an **inverse index** is to quickly search text documents with one or a few words.

- `GIN - Generalized Inverted Indexes`: Used for indexing composite values, such as arrays and JSONB. They allow for efficient searching of individual elements within the composite values.
- `GiST - Generalized Search Tree Indexes`: Used for indexing complex data types, such as geometric data and full-text search. They allow for efficient searching of spatial and textual data.
- `SP-GiST - Space-Partitioned Generalized Search Tree Indexes`: Used for indexing data that can be partitioned into non-overlapping regions, such as spatial data. They allow for efficient searching of spatial data by partitioning the space into non-overlapping regions.
