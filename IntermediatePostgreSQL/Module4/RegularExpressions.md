# Notes on Regular Expressions in PostgreSQL

---

## Regular Expressions

---

- A text based programming language
- Clever wild-card strings for matching and parsing text
- Widely available
  - Unix commands like `grep`
  - Virtually every programming language
  - Subtle differences across implementations
- PostgreSQL uses the POSIX variant

---

## Understanding Regular Expressions

---

- Very powerful and quite cryptic at first.
- Fun once you understand them
- It is like learning a new programming language where marker characters are keywords
- It is kind of a throwback to the 1970's - very compact
- Lots of `StackOverflow` posts to look at ☺

---

## Regular Expression Quick Guid

---

- `^` - Matches the begining of a line
- `$` - Matches the end of a line
- `.` - Matches any single character
- `*` - Repeats a character zero or more times
- `*?` - Repeats a character zero or more times, but non-greedy (matches as little as possible)
- `+` - Repeats a character one or more times
- `+?` - Repeats a character one or more times, but non-greedy (matches as little as possible)
- `[aeiou]` - Matches any one of the characters in the brackets
- `[^XYX]` - Matches any one character that is not in the brackets
- `[a-z0-9]` - Matches any one character in the range of characters in the brackets
- `\d` - Matches any single digit character
- `(` - Indicates where string extraction is to start
- `)` - Indicates where string extraction is to end

---

## POSIX Regular Expressions in PostgreSQL

---

- `~` - Matches a regular expression, case sensitive
- `~*` - Matches a regular expression, case insensitive
- `!~` - Does not match a regular expression, case sensitive
- `!~*` - Does not match a regular expression, case insensitive
- Different than LIKE - Match anywhere
  - `tweet ~ 'UMSI'`
  - `tweet LIKE '%UMSI%'`

---

## The simplest regular expression (regex) is like `LIKE`

---

### Create table and store some data

```sql
CREATE TABLE em (id serial, primary key (id), email text);

INSERT INTO em (email)
VALUES
('csev@umich.edu'),
('coleen@umich.edu'),
('sally@uiuc.edu'),
('ted79@umuc.edu'),
('glenn1@apple.com'),
('nbody@apple.com');
```

```sh
discuss=# CREATE TABLE em (id serial, primary key (id), email text);

discuss=# INSERT INTO em (email)
VALUES
('csev@umich.edu'),
('coleen@umich.edu'),
('sally@uiuc.edu'),
('ted79@umuc.edu'),
('glenn1@apple.com'),
('nbody@apple.com');
INSERT 0 6
```

### Match any email that has `umich` in it

```sh
discuss=# select * from em where email ~ 'umich';
 id |      email
----+------------------
  7 | csev@umich.edu
  8 | coleen@umich.edu
(2 rows)
```

### Match any email that starts with `c`

```sh
discuss=# SELECT email FROM em WHERE email ~ '^c';
      email
------------------
 csev@umich.edu
 coleen@umich.edu
(2 rows)
```

### Match any email that ends with `edu`

```sh
discuss=# SELECT email FROM em WHERE email ~ 'edu$';
      email
------------------
 csev@umich.edu
 coleen@umich.edu
 sally@uiuc.edu
 ted79@umuc.edu
(4 rows)
```

### Match any email that starts with `g` or `n` or `t`

```sh
discuss=# SELECT email FROM em WHERE email ~ '^[gnt]';
      email
------------------
 ted79@umuc.edu
 glenn1@apple.com
 nbody@apple.com
(3 rows)
```

### Match any email that has a digit in it

```sh
discuss=# SELECT email FROM em WHERE email ~ '[0-9]';
      email
------------------
 ted79@umuc.edu
 glenn1@apple.com
(2 rows)
```

### Match any email that has two digits in a row

```sh
discuss=# SELECT email FROM em WHERE email ~ '[0-9][0-9]';
     email
----------------
 ted79@umuc.edu
(1 row)
```
