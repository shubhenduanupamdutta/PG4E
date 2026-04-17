# Initial Database Setup For the Course

---

## Setting Up Database Using `psql` CLI

To set up the database for the course, you can use the `psql` command-line interface (CLI) to connect to the PostgreSQL database and create a new user and database for the course. Credentials for the database are somewhere else, but the command will be

```sh
psql -h pg.pg4e.com -p 5432 -U <username here> -d <database name here>
```

`-h` is the flag for the host, `-p` is the flag for the port, `-U` is the flag for the username, and `-d` is the flag for the database name. After running this command, you will be prompted to enter the password for the user. Once you have entered the password, you will be connected to the database and you can run SQL queries against it.

```sh
Password for user pg4e_135aca6452:
psql (16.13 (Ubuntu 16.13-0ubuntu0.24.04.1), server 11.7 (Ubuntu 11.7-2.pgdg18.04+1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

pg4e_135aca6452=>
```

### Inserting SQL command from a file

```sh
pg43_<username>=> \i <filename here>
```

This command will execute the SQL commands in the file. This is a convenient way to run multiple SQL commands at once, especially if you have a lot of commands to run. You can create a SQL file with all the commands you want to run and then use the `\i` command to execute them all at once.
Filename should be relative to the current directory. So if you are in the home directory and your file is in the `Documents` directory, you can use `\i Documents/<filename here>` to execute the commands in the file.
