"""Get data from the web and put it into a PostgreSQL database."""

# https://www.pg4e.com/code/gmane.py
# https://www.pg4e.com/code/datecompat.py
# https://www.pg4e.com/code/myutils.py

# https://www.pg4e.com/code/hidden-dist.py
# copy hidden-dist.py to hidden.py
# edit hidden.py and put in your credentials

# python3 gmane.py
# Pulls data from the web and puts it into messages table

import re
import time
from typing import Final

import psycopg
import requests
from date_compatibility import parse_mail_date
from load_env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, USERNAME
from my_utils import query_value
from psycopg.sql import SQL

HTTP_OK: Final[int] = 200
MAX_RETRY: Final[int] = 5
CONNECTION_STRING: Final[str] = (
    f"postgresql://{USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
conn = psycopg.connect(CONNECTION_STRING)
cur = conn.cursor()

baseurl = "http://mbox.dr-chuck.net/sakai.devel/"

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL,
        email TEXT,
        sent_at TIMESTAMPTZ,
        subject TEXT,
        headers TEXT,
        body TEXT
    );
    """,
)

# Pick up where we left off
sql = SQL("SELECT max(id) FROM messages")
query_result = query_value(cur, sql)
start: int = 0 if query_result is None else query_result
print("Starting at", start)

many = 0
count = 0
fail = 0
while True:
    if many < 1:
        conn.commit()
        sval = input("How many messages:")
        if len(sval) < 1:
            break
        many = int(sval)

    start = start + 1

    # Skip rows that are already retrieved
    sql = SQL("SELECT id FROM messages WHERE id=%s")
    row = query_value(cur, sql, (start,))
    if row is not None:
        continue  # Skip rows that already exist

    many = many - 1
    url = f"{baseurl}{start}/{start + 1}"

    text = "None"
    try:
        # Open with a timeout of 30 seconds
        response = requests.get(url, timeout=30)
        text = response.text
        status = response.status_code
        if status != HTTP_OK:
            print("Error code=", status, url)
            break
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

    print(url, len(text))
    count = count + 1

    if not text.startswith("From "):
        print(text)
        print("Did not find From ")
        fail = fail + 1
        if fail > MAX_RETRY:
            break
        continue

    pos = text.find("\n\n")
    if pos > 0:
        hdr = text[:pos]
        body = text[pos + 2 :]
    else:
        print(text)
        print("Could not find break between headers and body")
        fail = fail + 1
        if fail > MAX_RETRY:
            break
        continue

    # Accept with or without < >
    email = None
    x = re.findall("\nFrom: .* <(\\S+@\\S+)>\n", hdr)
    if len(x) == 1:
        email = x[0]
        email = email.strip().lower()
        email = email.replace("<", "")
    else:
        x = re.findall("\nFrom: (\\S+@\\S+)\n", hdr)
        if len(x) == 1:
            email = x[0]
            email = email.strip().lower()
            email = email.replace("<", "")

    sent_at = None
    y = re.findall("\nDate: .*, (.*)\n", hdr)
    if len(y) == 1:
        tdate = y[0]
        tdate = tdate[:26]
        sent_at = parse_mail_date(tdate)
        if not sent_at:
            print(text)
            print("Parse fail", tdate)
            fail = fail + 1
            if fail > MAX_RETRY:
                break
            continue

    subject = None
    z = re.findall("\nSubject: (.*)\n", hdr)
    if len(z) == 1:
        subject = z[0].strip().lower()

    # Reset the fail counter
    fail = 0
    print("   ", email, sent_at, subject)
    cur.execute(
        """
        INSERT INTO messages (id, email, sent_at, subject, headers, body)
        VALUES ( %s, %s, %s, %s, %s, %s )
        ON CONFLICT DO NOTHING
        """,
        (start, email, sent_at, subject, hdr, body),
    )
    if count % 50 == 0:
        conn.commit()
    if count % 100 == 0:
        time.sleep(1)

conn.commit()
cur.close()
conn.close()
