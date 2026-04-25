# Notes on Character Sets in PostgreSQL

---

## Representing Simple Strings

---

- **In the Old Days** - each character is represented by a number between 0 and 127 stored in 8 bits of memory.
- We refer to **8 bits of memory as a _byte_ of memory**.
- The `ascii()` function tells us the numeric value of a single ASCII character.
- The `chr()` function maps from an integer to a character.

```sh
discuss=# SELECT ascii('H'), ascii('e'), ascii('l'), chr(72), chr(42);
 ascii | ascii | ascii | chr | chr
-------+-------+-------+-----+-----
    72 |   101 |   108 | H   | *
(1 row)
```

---

## Beyond 127

---

- To be **more international** they defined characters 128-255 but inconsistently.
- This made second half of the 256 character set unusable for international use and across programs.

### Overlapping character set

- We needed more than 128 characters globally so 128-255 could mean different things based on context
  - **ISO 8859-2** - For eastern European languages
  - **ISO 8859-3** - For Turkish, Maltese, and Esperanto
  - **ISO 8859-5** - For Cyrillic languages and so on

- But these were not self-documenting you needed to know the character set outside the data of the file -- _Confusion!_

---

## Unicode - All characters in One Set

---

- Unicode is 32/21 bits (long story)
- Unicode 12.1
  - 137,000 characters
  - 150 character sets

```sh
discuss=# SELECT chr(72), chr(231), chr(20013);
 chr | chr | chr
-----+-----+-----
 H   | ç   | 中
(1 row)
```

---

## But we can't afford 32 bit characters

---

**`UTF-8` is a compression schema for Unicode which uses 1-4 bytes per character.**

- Represents 21 bits in 8-32 bits
- 0-127 are ASCII characters and take 1 byte
- 128-255 are signals to inform that the next 1-3 bytes are part of the same character

---

## UTF-8 Designed for Transition

---

- Pure ASCII is UTF-8 / no conversion
- Partial auto detect/convert of
  - Latin-1 variants
  - 1252 variants

### UTF-8 is dominant

- Rapid uptake after 2004
- UTF-8 is 94% of all web pages in 2019.
