# Notes on SQL Architecture

---

## Using SQL

---

An user can connect to the PostgreSQL using `pgAdmin` (Browser/Desktop) GUI or `psql` CLI. Both of these tools will allow you to connect to the PostgreSQL database and run SQL queries against it. In this course we will be using `psql` CLI to connect to the PostgreSQL database and run SQL queries against it.

### Starting PostgreSQL Command Line

```sh
$ psql -U postgres
Password for user postgres: <password here>
psql (9.3.5, server 11.2)
Type "help" for help.

postgres=#
```

`#` sign is Unix way of saying that you are logged in as a superuser. In this case, we are logged in as `postgres` user, which is the default superuser for PostgreSQL.

### Creating a User and Database

```sh
postgres=# CREATE USER pg4e WITH PASSWORD `secret`;
CREATE ROLE
postgres=# CREATE DATABASE people WITH OWNER 'pg4e';
CREATE DATABASE
postgres=# \q
```

This will create a new user called `pg4e` with the password `secret` and a new database called `people` owned by the user `pg4e`. After running these commands, you can connect to the `people` database using the `pg4e` user and run SQL queries against it.
`\q` is the command to quit the `psql` CLI.
You can use small letters for commands and keywords, but it is a common convention to use capital letters for SQL commands and keywords to make them stand out from the rest of the text. It is not required, but it is a good practice to follow.

### Connecting to a Database

```sh
$ psql people pg4e
Password for user pg4e: <password here>
psql (9.3.5, server 11.2)

people=> \dt
No relations found.
people=>
```

This will connect to the `people` database using the `pg4e` user and run the `\dt` command to list all the tables in the database. Since we haven't created any tables yet, it will return `No relations found.`
`people=>` doesn't end with `#` because we are not logged in as a superuser, we are logged in as a regular user.

**You want to make sure that you are doing as little as possible as a superuser. You want to do as much as possible as a regular user.** This is a good security practice because it limits the damage that can be done if your account is compromised. If you are logged in as a superuser and your account is compromised, the attacker can do anything they want to the database, including deleting all the data. If you are logged in as a regular user and your account is compromised, the attacker can only do what that user is allowed to do, which is usually much less than what a superuser can do.

### Create a Table

```sh
people=> CREATE TABLE users(
people(> name VARCHAR(128),
people(> email VARCHAR(128)
people(> );
CREATE TABLE
people=> \dt
          List of relations
 Schema | Name  | Type  | Owner
--------+-------+-------+-------
    public | users | table | pg4e
    (1 row)
```

There is also `\d+ users` command to get more details about the `users` table. It will show you the columns in the table, their data types, and any constraints on the columns.

---

Any constrains you provide is strictly followed. Because Postgres does all its work to optimize the structure by the constraints you provide.
