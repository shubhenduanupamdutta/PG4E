# Notes on Data Types in PostgreSQL

---

## Looking at Data Types

---

- **Text Fields (small and large)**
- **Binary Fields (small and large)**
- **Numeric Fields (integers and floating point)**
- **AUTO_INCREMENT Fields**

---

## String Fields

---

- Understand character sets and are indexable for searching.
- `CHAR(n)` allocates the entire space (faster for small strings where length is known).
- `VARCHAR(n)` allocates a variable amount of space depending on the data length (less space).

---

## Text Fields

---

- Have a character set - paragraphs or HTML pages
  - `TEXT` varying length
- Generally not used with indexing or sorting - and only then limited to a prefix
- Also understand characters sets

---

## Binary Types (rarely used)

---

- Character: 8 - 32 bits of information depending on character set
- Bytes = 8 bits of information
- `BYTEA(n)` up to 255 bytes
- Small Images - data
- Not indexed or sorted
- This doesn't understand character sets - just raw data

---

## Integer Numbers

---

**Integer numbers are very efficient, take little storage, and are easy to process because CPUs can often compare them with a single instruction.**

- `SMALLINT` - 2 bytes, range: -32,768 to 32,767
- `INTEGER` (or `INT`) - 4 bytes, range: -2,147,483,648 to 2,147,483,647
- `BIGINT` - 8 bytes, range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807

---

## Floating Point Numbers

---

**Floating point numbers can represent a wide range of values, but accuracy is limited.**

- `REAL`- (32 bit) 10<sup>38</sup> with seven digits of precision
- `DOUBLE PRECISION` - (64 bit) 10<sup>308</sup> with 15 digits of precision, usually used in scientific calculations and simulations.
- `NUMERIC(accuracy, decimal)` - user defined precision and scale. Specified digits of accuracy and digits after the decimal point. Can be used for financial calculations where precision is important.

---

## Dates

---

- `TIMESTAMP` - "YYYY-MM-DD HH:MM:SS" format. It is basically a 64-bit number and it represents minutes and seconds form 4173 BC to 294276 AD. It is used for storing date and time information. Years ago it was stored as a 32-bit number and it represented seconds from 1970 to 2038. But now it is stored as a 64-bit number and it can represent a much wider range of dates.
- `DATE` - "YYYY-MM-DD" format.
- `TIME` - "HH:MM:SS" format.
- Built-in PostgreSQL function `NOW()` returns the current date and time as a `TIMESTAMP` value.
