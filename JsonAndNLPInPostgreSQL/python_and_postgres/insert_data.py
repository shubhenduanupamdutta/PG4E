"""Assignment 2: Insert data into PostgreSQL using psycopg.

In this assignment, you will write a Python program to insert a sequence of 300 pseudorandom
numbers into a database table named pythonseq with the following schema:

CREATE TABLE pythonseq (iter INTEGER, val INTEGER);
You should drop and recreate the pythonseq table each time your application runs.
"""

from collections.abc import Generator
from typing import Final

import hidden
import psycopg
from psycopg.sql import SQL

# Load the secrets
secrets = hidden.secrets()

# Connect to the database
CONNECTION_STRING: Final[str] = (
    f"postgresql://{secrets['user']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['database']}"
)


def get_pseudorandom_number(amount: int = 300) -> Generator[int]:
    """Generate a pseudorandom number."""
    number = 463376
    for i in range(amount):
        print(i + 1, number)
        yield number
        number = int((number * 22) / 7) % 1_000_000


def insert_data(amount: int) -> None:
    """Insert pseudorandom numbers into the database."""
    conn = psycopg.connect(CONNECTION_STRING)

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS pythonseq CASCADE;")
    cur.execute("CREATE TABLE pythonseq (iter INTEGER, val INTEGER);")
    conn.commit()

    sql = SQL("INSERT INTO pythonseq (iter, val) VALUES (%s, %s);")
    for i, number in enumerate(get_pseudorandom_number(amount)):
        cur.execute(sql, (i + 1, number))
        if i % 50 == 0:
            print("Inserted", i + 1, "records...")
            conn.commit()

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    insert_data(300)
