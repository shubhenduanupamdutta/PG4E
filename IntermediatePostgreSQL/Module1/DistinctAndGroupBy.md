# Notes on Distinct and Group By

---

## `DISTINCT` and `GROUP BY` Keyword

---

### Reducing the result set

- `DISTINCT` only returns unique rows in a result set - and row will only appear once
- `DISTINCT ON` limits duplicate removal to a set of columns
- `GROUP BY` is combined with aggregate functions like `COUNT()`, `MAX()`, `SUM()`, `AVE()`, etc. to group rows based on column values and perform calculations on those groups.
- `DISTINCT` and `GROUP BY` happens after `JOIN`s and `WHERE` filtering, but before `ORDER BY` and `LIMIT`.

---

## `DISTINCT` vs `DISTINCT ON`

---

```sql
SELECT DISTINCT model FROM racing;
```

This query focuses on the `model` column, and it will return a list of unique car models from the `racing` table. If there are multiple rows with the same model, only one of those rows will be included in the result set. All other columns are not in consideration for uniqueness in this case, so the result will only show distinct values of the `model` column.

```sql
SELECT DISTINCT ON (model) make, model FROM racing;
```

This query also focuses on the `model` column for determining uniqueness, but it will return the first occurrence of each unique model along with its corresponding make. The `DISTINCT ON (model)` clause ensures that only one row per unique model is returned, and the specific row that is returned for each model will be the first one encountered in the result set based on the order of the data in the table.

---

## Aggregate / `GROUP BY`

---

```sh
pg4e=# SELECT COUNT(abbrev), abbrev FROM pg_timezone_names GROUP by abbrev LIMIT 10;
 count | abbrev
-------+--------
     1 | +00
     1 | PST
     2 | IST
     4 | -01
     2 | HST
     6 | +09
    17 | +05
     6 | ADT
     1 | +1245
     1 | -12
(10 rows)
```

- There will be no replication of `abbrev` in the result set, because we are grouping by `abbrev`. Each row in the result set will represent a unique value of `abbrev`, and the `COUNT(abbrev)` will show how many times that particular `abbrev` appears in the `pg_timezone_names` table.

### `WHERE` clause and `GROUP BY`

Let's see the following query:

```sh
pg4e=# SELECT COUNT(abbrev) AS ct, abbrev FROM pg_timezone_names
WHERE is_dst='t' GROUP BY abbrev HAVING COUNT(abbrev) > 10;
 ct | abbrev
----+--------
 17 | EEST
 14 | CDT
 34 | CEST
 20 | EDT
(4 rows)
```

- The `WHERE` clause filters the rows before the grouping happens, so only rows where `is_dst='t'` are considered for the `GROUP BY` operation. This means that the count of `abbrev` will only include those rows where `is_dst` is true, and the result will show how many times each unique `abbrev` appears in the filtered dataset. The `HAVING` clause then further filters the grouped results to only include those groups where the count of `abbrev` is greater than 10.

- `HAVING` is like a `WHERE` clause which happens after the calculation.
