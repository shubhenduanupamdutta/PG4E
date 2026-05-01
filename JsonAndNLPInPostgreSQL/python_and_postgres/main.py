"""Sample Connection to PostgreSQL using psycopg and dotenv."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Final

from dotenv import load_dotenv
from psycopg import AsyncConnection, AsyncCursor, Connection

# Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv("LOCAL_DB_USERNAME")
DB_NAME = "natural_language"
DB_HOST = os.getenv("LOCAL_DB_HOST")
DB_PORT = os.getenv("LOCAL_DB_PORT")
DB_PASSWORD = os.getenv("LOCAL_DB_PASSWORD")

CONNECTION_STRING: Final[str] = (
    f"postgresql://{USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


@asynccontextmanager
async def get_async_connection() -> AsyncGenerator[AsyncConnection]:
    """Get an asynchronous connection to the PostgreSQL database."""
    async_connection: AsyncConnection = await AsyncConnection.connect(CONNECTION_STRING)
    try:
        yield async_connection
    finally:
        await async_connection.close()


async def execute_query() -> Any:
    """Execute a query and return the results."""
    query = "SELECT * FROM docs ORDER BY id LIMIT 3"
    async with get_async_connection() as connection, connection.cursor() as cursor:
        await cursor.execute(query)
        return await cursor.fetchall()


async def main() -> None:
    """Execute the query and prints the results."""
    results = await execute_query()
    for row in results:
        print(row)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# PG4E/JsonAndNLPInPostgreSQL/python_and_postgres [ main][!+][📦 v0.1.0][🐍 v3.13.12(pg4e)]
# x python main.py
# (1, 'This is SQL and Python and other fun teaching stuff')
# (2, 'More people should learn SQL from UMSI')
# (3, 'UMSI also teaches Python and also SQL')
