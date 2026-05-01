# Noes on Ranking Search Results in PostgreSQL

---

## Introduction

---

- You don't have to rank the results but many times you will want to.
- Important to note that ranking happens in `SELECT` clause and not in `WHERE` clause. This is because `WHERE` clause filters the results and only after that we can rank the results.
- `WHERE` clause decides computation time. For example filtering out 100 rows from 1 million rows data will take more time than ranking and sorting 100 rows.
- We will be using previously filled up table `messages` from `Mail Archive` demo.

---

## Ranking using `ts_rank` function

---

The `ts_rank` function is used to rank the search results based on the relevance of the search query to the text data. It takes two arguments: a `tsvector` and a `tsquery`. The `tsvector` is a preprocessed version of the text data, and the `tsquery` is the search query. The `ts_rank` function returns a floating-point number that represents the relevance of the search query to the text data. The higher the number, the more relevant the search query is to the text data.

### Example SQL statement for ranking search results using `ts_rank` function

```sql
SELECT id, subject, sender, ts_rank(to_tsvector('english', body), to_tsquery('english', 'personal & learning')) AS ts_rank
FROM messages
WHERE to_tsquery('english', 'personal & learning') @@ to_tsvector('english', body)
ORDER BY ts_rank DESC;
```

In this example, we are selecting the `id`, `subject`, `sender`, and the relevance score calculated by the `ts_rank` function for each message in the `messages` table. We are filtering the results using the `WHERE` clause to only include messages that match the search query 'personal & learning'. Finally, we are ordering the results by the relevance score in descending order, so that the most relevant messages appear first.

```sh
python_postgres=# SELECT id, subject, sender, ts_rank(to_tsvector('english', body), to_tsquery('english', 'personal & learning')) AS ts_rank
FROM messages
WHERE to_tsquery('english', 'personal & learning') @@ to_tsvector('english', body)
ORDER BY ts_rank DESC;
 id  |                               subject                                |           sender           |   ts_rank
-----+----------------------------------------------------------------------+----------------------------+--------------
   4 | re: lms/vle rants/comments                                           | Michael.Feldstein@suny.edu |   0.28235176
   5 | re: lms/vle rants/comments                                           | john@caret.cam.ac.uk       |   0.09148999
   7 | re: lms/vle rants/comments                                           | john@caret.cam.ac.uk       |   0.09148999
 396 | re: siteservice.getsite.getmembers returns different list than  what | marquard@ched.uct.ac.za    | 0.0058589773
 209 | re: web services delegates and documentation                         | csev@umich.edu             | 2.220446e-16
 186 | re: web services delegates and documentation                         | s-githens@northwestern.edu | 2.220446e-16
 221 | re: web services delegates and documentation                         | shaneosullivan1@gmail.com  | 2.220446e-16
 330 | re: web services delegates and documentation                         | shaneosullivan1@gmail.com  | 2.220446e-16
  92 | re: resources tool                                                   | SinouVivian@foothill.edu   |        1e-16
(9 rows)
```

---

## Ranking using `ts_rank_cd` function

---

The `ts_rank_cd` function is similar to the `ts_rank` function, but it uses a different algorithm for calculating the relevance score. The `ts_rank_cd` function takes into account the distance between the search query and the text data, as well as the frequency of the search query in the text data. This can result in a more accurate relevance score for certain types of search queries.

### Example SQL statement for ranking search results using `ts_rank_cd` function

```sql
SELECT id, subject, sender, ts_rank_cd(to_tsvector('english', body), to_tsquery('english', 'personal & learning')) AS ts_rank_cd
FROM messages
WHERE to_tsquery('english', 'personal & learning') @@ to_tsvector('english', body)
ORDER BY ts_rank_cd DESC;
```

```sh
python_postgres=# SELECT id, subject, sender, ts_rank_cd(to_tsvector('english', body), to_tsquery('english', 'personal & learning')) AS ts_rank_cd
FROM messages
WHERE to_tsquery('english', 'personal & learning') @@ to_tsvector('english', body)
ORDER BY ts_rank_cd DESC;
 id  |                               subject                                |           sender           |  ts_rank_cd
-----+----------------------------------------------------------------------+----------------------------+---------------
   4 | re: lms/vle rants/comments                                           | Michael.Feldstein@suny.edu |    0.13095137
   7 | re: lms/vle rants/comments                                           | john@caret.cam.ac.uk       |   0.021860465
   5 | re: lms/vle rants/comments                                           | john@caret.cam.ac.uk       |   0.021860465
 396 | re: siteservice.getsite.getmembers returns different list than  what | marquard@ched.uct.ac.za    |       0.00625
  92 | re: resources tool                                                   | SinouVivian@foothill.edu   | 0.00042194093
 221 | re: web services delegates and documentation                         | shaneosullivan1@gmail.com  | 0.00023474179
 330 | re: web services delegates and documentation                         | shaneosullivan1@gmail.com  | 0.00023474179
 209 | re: web services delegates and documentation                         | csev@umich.edu             | 0.00023474179
 186 | re: web services delegates and documentation                         | s-githens@northwestern.edu | 0.00023474179
(9 rows)
```

---

## Some Other General Ranking Functions

---

Example SQL

```sql
SELECT
    employee_id,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rnk
FROM employees;
```

In this example, we are selecting the `employee_id`, `department`, and `salary` from the `employees` table. We are also calculating three different ranking functions: `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`. These functions are used to assign a unique rank to each employee within their respective department based on their salary. The `PARTITION BY` clause is used to group the employees by department, and the `ORDER BY` clause is used to sort the employees within each department by salary in descending order.

- `ROW_NUMBER()` assigns a unique sequential integer to rows within a partition of a result set, starting at 1 for the first row in each partition.
- `RANK()` assigns a rank to each row within a partition of a result set, with gaps in the ranking values when there are ties.
- `DENSE_RANK()` assigns a rank to each row within a partition of a result set, without gaps in the ranking values when there are ties.

Example result of the above SQL statement:

```sh
 employee_id | department | salary | row_num | rnk | dense_rnk
-------------+------------+--------+---------+-----+-----------
           1 | Sales      | 70000  |       1 |   1 |         1
           2 | Sales      | 60000  |       2 |   2 |         2
           3 | Sales      | 60000  |       3 |   2 |         2
           4 | Sales      | 50000  |       4 |   4 |         3
           5 | Marketing  | 80000  |       1 |   1 |         1
           6 | Marketing  | 75000  |       2 |   2 |         2
           7 | Marketing  | 75000  |       3 |   2 |         2
           8 | Marketing  | 70000  |       4 |   4 |         3
           9 | IT         | 90000  |       1 |   1 |         1
          10 | IT         | 85000  |       2 |   2 |         2
```
