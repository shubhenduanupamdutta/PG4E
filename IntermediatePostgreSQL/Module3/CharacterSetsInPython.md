# Notes on Character Sets in Python

---

## Python 3 and Unicode

---

**One of the big transition of Python 2 vs Python 3** was the move to Unicode as the default character set.

- Strings in memory are Unicode, that means in memory they are stored in 4 bytes per character.
- The **bytes** type if for 8-bit characters.
- Strings **at rest** are generally stored UTF-8 for space and interoperability
  - Files
  - Network resources
  - Database Tables

### `encode()` and `decode()`

- `encode()` converts from Unicode to bytes
- `decode()` converts from bytes to Unicode

**This whole thing is required because in python memory strings are Unicode (4 bytes) so fully decompressed, but on disk and other resources they are stored in UTF-8 (1-4 bytes) so compressed. So to work with them in memory we need to decompress (`decode`) and to write them to disk we need to compress (`encode()`).**

---

## Opening files in Python

---

`open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)`

- `encoding` is the character set to use when reading/writing the file

---

## Database Data

---

- When you interact with database from Python all conversion between Unicode and UTF-8 is done implicitly.
- The python database connector (`psycopg` for PostgreSQL) knows the internal storage format of the database and does the conversion for you.
