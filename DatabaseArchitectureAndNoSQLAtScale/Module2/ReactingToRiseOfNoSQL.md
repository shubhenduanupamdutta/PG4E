# Notes on Reacting to Rise of NoSQL

---

## But That's Not All

---

- The ACID vendors saw market share slipping away circa 2013
- As NoSQL applications matured they found that application developers wanted "a few" transactions and JOINs
- ACID + BASE became the new sweet spot

---

## Technology Changes 2009-2019

---

- AWS could sell you 32 CPU systems with large amounts of RAM cheaper than you could own them
- Solid State Disk developed scatter/gather on a single drive with 32+ simultaneous reads to different areas of the drive.
- Basically if you want you can vertically scale to a large capacity.
- Ability to scale RDBMS limit has become higher.

---

## RDBMS Vendors React

---

### Oracle

- JSON Columns
- NoSQL features

### MySQL 8.0

- JSON Columns

### PostgreSQL

- 8.3 HSTORE Columns (2008 & 2014)
- 9.2 JSON Columns (2012)
- 9.4 JSONB Columns (2014)

### Amazon Redshift

- Based on a _modified_ PostgreSQL 8.0 (2013)

---

## ACID + BASE or BASE + ACID

---

- It turns out to be easier to relax ACID than to do the R&D to implement ACID in a system that is distributed at its core.
- SQL doesn't imply ACID
- BASE runtime databases are adopting SQL syntax for some of their operations to make it easier for developers to use them.
- SQL with ACID semantics or SQL with BASE semantics. Both are possible.

---

## Being Base-Like in ACID RDBMS

---

- **Do not normalize - Replicate**
- **Don't use SERIAL - use UUID**
- **Columns are for indexing**
- **Do not use foreign keys or don't mark them as such**
- **Design your schema / indexes to enable reading a single row on query**
- **Use software migrations instead of ALTER**
- **Query for records by primary key or by indexed column**
- **Do not use JOINs**
- **Do not use aggregations (COUNT ??)**

---

## Summary

---

- NoSQL is doing well
  - More for specialized applications
  - Less conversation about the "end of SQL"
  - Breathless is becoming pragmatic
  - There is a learning curve - production experience
  - SASS from cloud vendors make it **easier**
- Some applications converting back
  - **Move from MongoDB to PostgreSQL**
