"""Loads environment variables from a .env file and prints them to the console."""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
USERNAME = os.environ["LOCAL_DB_USERNAME"]
DB_NAME = os.environ["LOCAL_DB_NAME"]
DB_HOST = os.environ["LOCAL_DB_HOST"]
DB_PORT = os.environ["LOCAL_DB_PORT"]
DB_PASSWORD = os.environ["LOCAL_DB_PASSWORD"]
