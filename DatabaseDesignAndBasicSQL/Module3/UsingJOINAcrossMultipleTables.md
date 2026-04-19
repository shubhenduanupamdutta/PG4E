# Notes on Using JOIN Across Multiple Tables

---

## Relational Power

---

- By removing the replicated data and replacing it with references to a single copy of each bit of data, we build a _web_ of information that the relational database can read through very quickly - even for very large amount of data.

- Often when you want some data it comes from a number of tables linked by these **foreign keys**.

---

## The `JOIN` Operation

---

### `INNER JOIN`

**By default `JOIN` is an `INNER JOIN` which means that it will only return rows where there is a match in both tables.**

- The `JOIN` operation _links across several tables_ as part of a `SELECT` operation.
- You must tell the JOIN **how to use the keys** that make the connection between the tables using an `ON` clause.

Dr. Chucks preference is to follow arrow direction. Many to one.

A standard JOIN statement looks like this:

```sql
SELECT track.title, album.title, artist.name, genre.name
FROM track
JOIN album ON track.album_id = album.id
JOIN artist ON album.artist_id = artist.id
JOIN genre ON track.genre_id = genre.id
```

### CROSS JOIN

- A `CROSS JOIN` is a type of join that returns the Cartesian product of the two tables being joined. This means that it will return all possible combinations of rows from both tables. For example, if you have a `track` table with 10 rows and an `album` table with 5 rows, a `CROSS JOIN` between these two tables would return 50 rows (10 x 5). It is important to use `CROSS JOIN` with caution, as it can result in a very large number of rows being returned if the tables being joined have a large number of rows.

A standard CROSS JOIN statement looks like this:

```sql
SELECT track.title, album.title
FROM track
CROSS JOIN album
```

`JOIN`s are not stored. In the last moment we just show to the user data from the tables in the format.
