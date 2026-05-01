"""Load a book into PostgreSQL and create a full text search index on it."""

# https://www.pg4e.com/code/loadbook.py
# https://www.pg4e.com/code/myutils.py

# Download a book
# wget http://www.gutenberg.org/cache/epub/19337/pg19337.txt

# (If needed)
# https://www.pg4e.com/code/hidden-dist.py
# copy hidden-dist.py to hidden.py
# edit hidden.py and put in your credentials

# python3 loadbook.py

import time
from pathlib import Path
from typing import Final

import psycopg
from load_env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, USERNAME
from psycopg.sql import SQL, Composed, Identifier

book_file = input("Enter book file (i.e. pg19337.txt): ")
if book_file == "":
    book_file = "pg19337.txt"
base = book_file.split(".")[0]

# Make sure we can open the file
file_handle = Path(book_file).open()  # noqa: SIM115
CONNECTION_STRING: Final[str] = (
    f"postgresql://{USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
conn = psycopg.connect(CONNECTION_STRING)

cur = conn.cursor()

sql: Composed = SQL("DROP TABLE IF EXISTS {} CASCADE;").format(Identifier(base))
print(sql.as_string(conn))
cur.execute(sql)

sql = SQL("CREATE TABLE {} (id SERIAL, body TEXT);").format(Identifier(base))
print(sql.as_string(conn))
cur.execute(sql)

para = ""
chars, count, operation_count = 0, 0, 0

for line in file_handle:
    count = count + 1
    cur_line = line.strip()
    chars = chars + len(cur_line)
    if cur_line == "" and para == "":
        continue
    if cur_line == "":
        sql = SQL("INSERT INTO {} (body) VALUES (%s);").format(Identifier(base))
        cur.execute(sql, (para,))
        operation_count += 1
        if operation_count % 50 == 0:
            conn.commit()
        if operation_count % 100 == 0:
            print(operation_count, "loaded...")
            time.sleep(1)
        para = ""
        continue

    para = para + " " + line

conn.commit()

print(" ")
print("Loaded", operation_count, "paragraphs", count, "lines", chars, "characters")

sql = SQL("CREATE INDEX {} ON {} USING gin(to_tsvector('english', body));").format(
    Identifier(f"{base}_gin"),
    Identifier(base),
)
print(sql.as_string(conn))
cur.execute(sql)
conn.commit()
cur.close()

conn.close()
file_handle.close()

# SELECT body FROM pg19337
# WHERE to_tsquery('english', 'goose') @@ to_tsvector('english', body)
# LIMIT 5;
#
# EXPLAIN ANALYZE SELECT body FROM pg19337
# WHERE to_tsquery('english', 'goose') @@ to_tsvector('english', body);
#
# EXPLAIN ANALYZE SELECT body FROM pg19337
# WHERE phraseto_tsquery('english', 'tiny tim') @@ to_tsvector('english', body);
