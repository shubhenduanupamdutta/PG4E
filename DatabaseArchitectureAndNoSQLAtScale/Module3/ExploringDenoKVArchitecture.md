# Notes on Exploring DenoKV Architecture Through B-Trees

---

## Deno KV Database Architecture (High Level)

---

### Deno _Actual_ Architecture Low Level

- Foundation DB
  - [GitHub Repository](https://github.com/apple/foundationdb)
  - AI: "Foundation DB Technical Overview"
- SQLite
  - [SQLite Homepage](https://sqlite.org)

### Deno KV Overview

**This need not be true**, it is to give a notion why Deno has chosen to go with KV store\_

- Organizes Schemaless JSON documents
- No explicit tables
- Keys
  - Hierarchical logical key
  - No Integer, GUID, or SERIAL primary keys
  - Logical keys are JavaScript Arrays
  - Data can be stored (set) or retrieved (get) by key
  - Data can be scanned by logical key prefix (list)
  - Only sort order is logical key order
- Similar to a PostgreSQL B-Tree index
- Deno KV is sorted dictionary (by key)

---

## Why B-Trees

---

**B-Trees** is a tree data structure that keeps data sorted and allows for efficient insertion, deletion, and search operations. It is a self-balancing tree that maintains sorted data and allows for logarithmic time complexity for search, insert, and delete operations.

### Distributed B-Trees

Deno KV is _likely_ some variation of a single large B-Tree structure spread across the Deno Deploy nodes at data centers around the world. The nodes are connected via a low-latency network to coordinate with each other.

- Pointers can be of node and block
- Links can be cross-server

---

## Summary

---

- B-Trees are a natural starting point for distributed eventual consistency database
- Logical keys only - no integer auto-incrementing keys
- Incrementing integers is not reliable in a distributed system
- The **ULID** (Universally Unique Lexicographically Sortable Identifier) is a special B-Tree friendly GUID.
