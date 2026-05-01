"""Load data from star wars API into PostgreSQL."""
# https://www.pg4e.com/code/swapi.py
# https://www.pg4e.com/code/myutils.py

# If needed:
# https://www.pg4e.com/code/hidden-dist.py
# copy hidden-dist.py to hidden.py
# edit hidden.py and put in your credentials

# python3 swapi.py
# Pulls data from the swapi.py4e.com API and puts it into our swapi table

import json
import time
from typing import Final

import my_utils
import psycopg
import requests
from load_env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, USERNAME
from psycopg.abc import QueryNoTemplate
from psycopg.rows import TupleRow
from psycopg.sql import SQL, Literal

MAX_RETRY: Final[int] = 5
CONNECTION_STRING: Final[str] = (
    f"postgresql://{USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def summary(cur: psycopg.Cursor[TupleRow]) -> None:
    """Print a summary of the data in the swapi table."""
    total = my_utils.query_value(cur, "SELECT COUNT(*) FROM swapi;")
    todo = my_utils.query_value(cur, "SELECT COUNT(*) FROM swapi WHERE status IS NULL;")
    good = my_utils.query_value(cur, "SELECT COUNT(*) FROM swapi WHERE status = 200;")
    error = my_utils.query_value(cur, "SELECT COUNT(*) FROM swapi WHERE status != 200;")
    print(f"Total={total} todo={todo} good={good} error={error}")


conn = psycopg.connect(CONNECTION_STRING)


cur = conn.cursor()

default_url: str = "https://swapi.py4e.com/api/films/1/"
print("If you want to restart the spider, run")
print("DROP TABLE IF EXISTS swapi CASCADE;")
print(" ")

sql: QueryNoTemplate = SQL(
    """
CREATE TABLE IF NOT EXISTS swapi (
    id serial,
    url VARCHAR(2048) UNIQUE,
    status INTEGER,
    body JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);
""",
)
print(sql)
cur.execute(sql)
conn.commit()  # Table is created

# Check to see if we have urls in the table, if not add starting points
# for each of the object trees
count = my_utils.query_value(cur, "SELECT COUNT(url) FROM swapi;")
if count is None or count < 1:
    objects = ["films", "species", "people"]
    for obj in objects:
        sql = SQL("INSERT INTO swapi (url) VALUES ( {} )").format(
            Literal(f"https://swapi.py4e.com/api/{obj}/1/"),
        )
        print(sql.as_string(conn))
        cur.execute(sql)
    conn.commit()

many = 0
count = 0
chars = 0
fail = 0
summary(cur)
while True:
    if many < 1:
        conn.commit()
        sval = input("How many documents:")
        if len(sval) < 1:
            break
        many = int(sval)

    url = my_utils.query_value(cur, "SELECT url FROM swapi WHERE status IS NULL LIMIT 1;")
    if url is None:
        print("All documents are retrieved.")
        break

    text = "None"
    try:
        print("=== Url is", url)
        response = requests.get(url, timeout=45)
        text = response.text
        print("=== Text is", text)
        status = response.status_code
        sql = "UPDATE swapi SET status=%s, body=%s, updated_at=NOW() WHERE url = %s;"
        row = cur.execute(sql, (status, text, url))
        count = count + 1
        chars = chars + len(text)
    except KeyboardInterrupt:
        print()
        print("Program interrupted by user...")
        break
    except requests.RequestException as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)
        fail = fail + 1
        if fail > MAX_RETRY:
            break
        continue

    todo = my_utils.query_value(cur, "SELECT COUNT(*) FROM swapi WHERE status IS NULL;")
    print(status, len(text), url, todo)

    try:
        js = json.loads(text)
    except json.JSONDecodeError as e:
        print("Unable to parse JSON", url)
        print("Error", e)
        continue

    # Look through all of the "linked data" for other urls to retrieve
    links = ["films", "species", "vehicles", "starships", "characters"]
    for link in links:
        stuff = js.get(link)
        if not isinstance(stuff, list):
            continue
        for item in stuff:
            sql = "INSERT INTO swapi (url) VALUES ( %s ) ON CONFLICT (url) DO NOTHING;"
            cur.execute(sql, (item,))

    many = many - 1
    if count % 25 == 0:
        conn.commit()
        print(count, "loaded...")
        time.sleep(1)
        continue

print(" ")
print(f"Loaded {count} documents, {chars} characters")

summary(cur)

print("Closing database connection...")
conn.commit()
cur.close()
conn.close()
