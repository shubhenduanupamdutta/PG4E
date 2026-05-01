"""Some utility functions to make it easier to work with PostgreSQL in Python."""

from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import QueryNoTemplate
from psycopg.errors import Error
from psycopg.rows import TupleRow

type IntReturns = Literal[
    "SELECT COUNT(url) FROM swapi;",
    "SELECT COUNT(*) FROM swapi;",
    "SELECT COUNT(*) FROM swapi WHERE status IS NULL;",
    "SELECT COUNT(*) FROM swapi WHERE status = 200;",
    "SELECT COUNT(*) FROM swapi WHERE status != 200;",
]

type StrReturns = Literal["SELECT url FROM swapi WHERE status IS NULL LIMIT 1;",]


@overload
def query_value(
    cur: Cursor,
    sql: IntReturns,
    fields: tuple[Any] | None = None,
    error: Error | None = None,
) -> int | None: ...
@overload
def query_value(
    cur: Cursor,
    sql: StrReturns,
    fields: tuple[Any] | None = None,
    error: Error | None = None,
) -> str | None: ...


def query_value(
    cur: Cursor,
    sql: QueryNoTemplate,
    fields: tuple[Any] | None = None,
    error: Error | None = None,
) -> int | str | None:
    """Query the database and return a single value or None if there was an error."""
    row = query_row(cur, sql, fields, error)
    if row is None:
        return None
    return row[0]


def query_row(
    cur: Cursor,
    sql: QueryNoTemplate,
    fields: tuple[Any] | None = None,
    error: Error | None = None,
) -> TupleRow | None:
    """Query the database and return a single row or None if there was an error."""
    _row = do_query(cur, sql, fields)
    try:
        row: TupleRow | None = cur.fetchone()
    except Error as e:
        if error:
            print(error, e)
        else:
            print(e)
        return None
    else:
        return row


def do_query(
    cur: Cursor,
    sql: QueryNoTemplate,
    fields: tuple[Any] | None = None,
) -> Cursor[TupleRow]:
    """Return a cursor with the results of the query."""
    return cur.execute(sql, fields)
