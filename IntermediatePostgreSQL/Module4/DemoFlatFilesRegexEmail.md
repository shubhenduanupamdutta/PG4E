# Notes on Demo: Flat Files, Regular Expressions and Email

---

**Get the data file `mbox-short.txt` from [Course Website](https://www.pg4e.com/lectures/mbox-short.txt)**
or you can use

```sh
wget https://www.pg4e.com/lectures/mbox-short.txt
```

---

## Create and add data to the table

---

```sql
CREATE TABLE mbox (line TEXT);
\copy mbox FROM 'mbox-short.txt' WITH DELIMITER E'\007';
```

### Character `E\'007'` is used as a delimiter to read the whole data as a single column value, this doesn't appear in the data file but is used to read the whole line as a single value

```sh
demo_regex=# \copy mbox FROM 'mbox-short.txt' WITH DELIMITER E'\007';
COPY 1910
```

### We can also directly download the data file and read it

```sh
demo_regex=# \copy mbox FROM PROGRAM 'wget -q -O - "$@" https://www.pg4e.com/lectures/mbox-short.txt' WITH DELIMITER E'\007';
```

- `-q -O - "$@"` is used to download the data file and read it directly without saving it to the disk.
- `-q` is used to suppress the output of the download process
- `-O -` is used to write the output to the standard output (stdout) instead of saving it to a file.
- `"$@"` is used to pass any additional arguments to the `wget` command if needed.

### Check the data

```sh
demo_regex=# SELECT * FROM mbox LIMIT 5;
                                line
--------------------------------------------------------------------
 From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
 Return-Path: <postmaster@collab.sakaiproject.org>
 Received: from murder (mail.umich.edu [141.211.14.90])
          by frankenstein.mail.umich.edu (Cyrus v2.3.8) with LMTPA;
          Sat, 05 Jan 2008 09:14:16 -0500
(5 rows)
```

---

## Do some queries on data with regex

---

### Lines which start with `From`

```sh
demo_regex=# SELECT line FROM mbox WHERE line ~ '^From';
                            line
-------------------------------------------------------------
 From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
 From: stephen.marquard@uct.ac.za
 From louis@media.berkeley.edu Fri Jan  4 18:10:48 2008
 From: louis@media.berkeley.edu
 From zqian@umich.edu Fri Jan  4 16:10:39 2008
 From: zqian@umich.edu
 From rjlowe@iupui.edu Fri Jan  4 15:46:24 2008
 From: rjlowe@iupui.edu
 From zqian@umich.edu Fri Jan  4 15:03:18 2008
 From: zqian@umich.edu
 From rjlowe@iupui.edu Fri Jan  4 14:50:18 2008
 From: rjlowe@iupui.edu
 From cwen@iupui.edu Fri Jan  4 11:37:30 2008
 From: cwen@iupui.edu
 From cwen@iupui.edu Fri Jan  4 11:35:08 2008
 From: cwen@iupui.edu
 From gsilver@umich.edu Fri Jan  4 11:12:37 2008
 From: gsilver@umich.edu
 From gsilver@umich.edu Fri Jan  4 11:11:52 2008
 From: gsilver@umich.edu
 From zqian@umich.edu Fri Jan  4 11:11:03 2008
 From: zqian@umich.edu
 From gsilver@umich.edu Fri Jan  4 11:10:22 2008
 From: gsilver@umich.edu
 From wagnermr@iupui.edu Fri Jan  4 10:38:42 2008
 From: wagnermr@iupui.edu
 From zqian@umich.edu Fri Jan  4 10:17:43 2008
 From: zqian@umich.edu
 From antranig@caret.cam.ac.uk Fri Jan  4 10:04:14 2008
 From: antranig@caret.cam.ac.uk
 From gopal.ramasammycook@gmail.com Fri Jan  4 09:05:31 2008
 From: gopal.ramasammycook@gmail.com
 From david.horwitz@uct.ac.za Fri Jan  4 07:02:32 2008
 From: david.horwitz@uct.ac.za
 From david.horwitz@uct.ac.za Fri Jan  4 06:08:27 2008
 From: david.horwitz@uct.ac.za
 From david.horwitz@uct.ac.za Fri Jan  4 04:49:08 2008
 From: david.horwitz@uct.ac.za
 From david.horwitz@uct.ac.za Fri Jan  4 04:33:44 2008
 From: david.horwitz@uct.ac.za
 From stephen.marquard@uct.ac.za Fri Jan  4 04:07:34 2008
 From: stephen.marquard@uct.ac.za
 From louis@media.berkeley.edu Thu Jan  3 19:51:21 2008
 From: louis@media.berkeley.edu
 From louis@media.berkeley.edu Thu Jan  3 17:18:23 2008
 From: louis@media.berkeley.edu
 From ray@media.berkeley.edu Thu Jan  3 17:07:00 2008
 From: ray@media.berkeley.edu
 From cwen@iupui.edu Thu Jan  3 16:34:40 2008
 From: cwen@iupui.edu
 From cwen@iupui.edu Thu Jan  3 16:29:07 2008
 From: cwen@iupui.edu
 From cwen@iupui.edu Thu Jan  3 16:23:48 2008
 From: cwen@iupui.edu
(54 rows)
```

### Extracting email addresses from the lines which start with `From`

```sh
demo_regex=# SELECT substring(line, ' (.+@[^ ]+) ') FROM mbox WHERE line ~ '^From';
           substring
-------------------------------
 stephen.marquard@uct.ac.za

 louis@media.berkeley.edu

 zqian@umich.edu

 rjlowe@iupui.edu

 zqian@umich.edu

 rjlowe@iupui.edu

 cwen@iupui.edu

 cwen@iupui.edu

 gsilver@umich.edu

 gsilver@umich.edu

 zqian@umich.edu

 gsilver@umich.edu

 wagnermr@iupui.edu

 zqian@umich.edu

 antranig@caret.cam.ac.uk

 gopal.ramasammycook@gmail.com

 david.horwitz@uct.ac.za

 david.horwitz@uct.ac.za

 david.horwitz@uct.ac.za

 david.horwitz@uct.ac.za

 stephen.marquard@uct.ac.za

 louis@media.berkeley.edu

 louis@media.berkeley.edu

 ray@media.berkeley.edu

 cwen@iupui.edu

 cwen@iupui.edu

 cwen@iupui.edu

(54 rows)
```

### Extracting email addresses and their counts from the lines which start with `From`

```sql
SELECT substring(line, ' (.+@[^ ]+) '), count(substring(line, ' (.+@[^ ]+) ')) FROM mbox
    WHERE line ~ '^From'
    GROUP BY substring(line, ' (.+@[^ ]+) ')
    ORDER BY count(substring(line, ' (.+@[^ ]+) ')) DESC;
```

```sh
demo_regex=# SELECT substring(line, ' (.+@[^ ]+) '), count(substring(line, ' (.+@[^ ]+) ')) FROM mbox
    WHERE line ~ '^From'
    GROUP BY substring(line, ' (.+@[^ ]+) ')
    ORDER BY count(substring(line, ' (.+@[^ ]+) ')) DESC;
           substring           | count
-------------------------------+-------
 cwen@iupui.edu                |     5
 david.horwitz@uct.ac.za       |     4
 zqian@umich.edu               |     4
 louis@media.berkeley.edu      |     3
 gsilver@umich.edu             |     3
 rjlowe@iupui.edu              |     2
 stephen.marquard@uct.ac.za    |     2
 antranig@caret.cam.ac.uk      |     1
 wagnermr@iupui.edu            |     1
 gopal.ramasammycook@gmail.com |     1
 ray@media.berkeley.edu        |     1
                               |     0
(12 rows)
```

### Same extraction as above but with a subquery to avoid repeating the regex pattern multiple times

```sql
SELECT email, count(email) FROM
    (SELECT substring(line, ' (.+@[^ ]+) ') AS email FROM mbox WHERE line ~ '^From') AS subquery
    GROUP BY email
    ORDER BY count(email) DESC;
```
