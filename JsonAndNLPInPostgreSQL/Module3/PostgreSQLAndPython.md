# Notes on PostgreSQL and Python

---

## Connecting to a database and querying using python

---

### Code example at [main.py](../python_and_postgres/main.py)

To connect to a PostgreSQL database using Python, we can use the `psycopg` library. Below is an example of how to establish a connection, execute a query, and fetch results:

You can install in the project using

```sh
uv add "psycopg[binary]"
```

This will install `psycopg 3` which is the latest version of the library.
This supports async API as well as a sync API. In the code example, we are using async API.

---

## Other Operations using Python

---

### Actual code is in [example.py](../python_and_postgres/examples.ipynb)

_All the operations in the `examples.ipynb` are usings sync API._

---

## Reading a book (in `.txt` format) and loading it into PostgreSQL

---

### Code is at [loadbook.py](../python_and_postgres/loadbook.py)

In this case we read a book in `.txt` format, load into a PostgreSQL table making sure that each paragraph is a separate row in the table. We also create a GIN index on the `body` column of the table to enable efficient full-text search queries.

### A utility module is at `my_utils.py` which has some helper functions to read the book and split it into paragraphs

---
