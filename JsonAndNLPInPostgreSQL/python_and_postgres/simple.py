"""Solution to Assignment 1 of the PostgreSQL and Python module of the PG4E course.

In this assignment, you will get the code for https://www.pg4e.com/code/simple.py working. Download
these files using wget, curl or your browser.

wget https://www.pg4e.com/code/simple.py
wget https://www.pg4e.com/code/hidden-dist.py
"""
# install psycopg2 (if needed)
# pip3 install psycopg2    # (or pip)

# https://www.pg4e.com/code/simple.py

# https://www.pg4e.com/code/hidden-dist.py
# copy hidden-dist.py to hidden.py
# edit hidden.py and put in your credentials

# python3 simple.py

# To check the results, use psql and look at the
# pythonfun table

from typing import Final

import hidden
import psycopg

# Load the secrets
secrets = hidden.secrets()
CONNECTION_STRING: Final[str] = (
    f"postgresql://{secrets['user']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['database']}"
)
conn = psycopg.connect(CONNECTION_STRING)

cur = conn.cursor()

sql = "DROP TABLE IF EXISTS pythonfun CASCADE;"
print(sql)
cur.execute(sql)

sql = "CREATE TABLE pythonfun (id SERIAL, line TEXT);"
print(sql)
cur.execute(sql)

conn.commit()  # Flush it all to the DB server

for i in range(10):
    txt = "Have a nice day " + str(i)
    sql = "INSERT INTO pythonfun (line) VALUES (%s);"
    cur.execute(sql, (txt,))

conn.commit()

sql = "SELECT id, line FROM pythonfun WHERE id=5;"
print(sql)
cur.execute(sql)

row = cur.fetchone()
if row is None:
    print("Row not found")
else:
    print("Found", row)

sql = "INSERT INTO pythonfun (line) VALUES (%s) RETURNING id;"
cur.execute(sql, (txt,))
id = cur.fetchone()[0]
print("New id", id)

# Lets make a mistake
sql = "SELECT line FROM pythonfun WHERE mistake=5;"
print(sql)
cur.execute(sql)

conn.commit()
cur.close()
