# Exercise - Implementing Many to Many Relationship

Create and implement and verify all commands to implement Music library database with local postgres:16 container.
I have created the postgres:16 container using `docker-compose.yml` file. You can use the same file or create your own.

---

## Running the postgres:16 container

```sh
docker compose -f docker-compose.yml up -d
```

---

## Connect to the postgres:16 container

```sh
psql -h localhost -p 5432 -U shubhendu -d pg4e
```

You will be prompted for the password. Enter the password you set in the `docker-compose.yml` file.

---

## Create the database `music` and connect to it

```sh
pg4e=# CREATE DATABASE music;
CREATE DATABASE
pg4e=# \c music
You are now connected to database "music" as user "shubhendu".
```

---

## Creating all the tables

---

`create_music_tables.sql` file contains all the commands to create the tables for our music library database. You can run the file using the `\i` command in psql.
Make sure that you are connected to the `music` database before running the file.
Make sure that file is in the same directory where you are running the psql command.

```sh
music=# \i create_music_tables.sql
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
music=# \dt
          List of relations
 Schema |  Name  | Type  |   Owner
--------+--------+-------+-----------
 public | album  | table | shubhendu
 public | artist | table | shubhendu
 public | genre  | table | shubhendu
 public | track  | table | shubhendu
(4 rows)

```
