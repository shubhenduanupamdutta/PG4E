"""Assignment 1: Retrieve 100 data from PokeAPI."""

import json
import os
import time

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]
USERNAME = os.environ["DB_USERNAME"]

CONNECTION_STRING = f"postgresql://{USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

## Connect to the database
conn = psycopg.connect(CONNECTION_STRING)
cur = conn.cursor()

## Create the table to store the data
cur.execute("""
CREATE TABLE IF NOT EXISTS pokeapi (
    id INTEGER,
    body JSONB
);""")
conn.commit()

## Retrieve data from the PokeAPI and store it in the database
for i in range(1, 101):
    url = f"{BASE_URL}{i}"
    print(f"Retrieving data for Pokemon ID {i} from {url}...")
    response = requests.get(url, timeout=45)
    if response.status_code != 200:  # noqa: PLR2004
        print(f"Failed to retrieve data for Pokemon ID {i}. Status code: {response.status_code}")
        continue

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for Pokemon ID {i}. Error: {e}")
        continue

    cur.execute("INSERT INTO pokeapi (id, body) VALUES (%s, %s);", (i, json.dumps(data)))
    conn.commit()
    print(f"Data for Pokemon ID {i} stored in the database.")
    time.sleep(0.5)  # Sleep to avoid hitting API rate limits


## Close the database connection
print("Closing database connection...")
conn.commit()
cur.close()
conn.close()
