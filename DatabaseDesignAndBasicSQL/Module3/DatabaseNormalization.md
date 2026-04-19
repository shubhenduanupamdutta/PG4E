# Notes on Database Normalization

---

## Database Normalization (3NF)

---

**There is _tons_ of database theory - way too much to understand without excessive predicate calculus**

- **Do not replicate data.** Instead, reference data. Point at data
- Use **integers for keys** and for references.
- Add a special _key_ column to each table, which you will make reference to.

---

## Integer Reference Pattern

---

**We use integer columns in one table to reference (or look up) rows in another table.**

---
