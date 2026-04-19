# Cheat Sheet for Basic PostgreSQL Commands

---

- `\l` - List all databases
- `\c <database_name>` - Connect to a database
- `\dt` - List all tables in the current database
- `\d <table_name>` - Describe the structure of a table
- `\d+ <table_name>` - Describe the structure of a table with additional information
- `\i <file_name.sql>` - Execute SQL commands from a file
- `\h <SQL_command>` - Get help on a specific SQL command
- `\?` - List all available commands in the PostgreSQL command line interface
- `\copy` - Copy data between a file and a table
- `\q` - Quit the PostgreSQL command line interface
- `CREATE DATABASE <database_name>;` - Create a new database
- `DROP DATABASE <database_name>;` - Delete a database
- `CREATE TABLE <table_name> (column1 datatype, column2 datatype, ...);` - Create a new table
- `DROP TABLE <table_name>;` - Delete a table

---

## `\copy` command

---

Example usage of `\copy` command to import data from a CSV file into a PostgreSQL table:

```sql
\copy track_raw(title,artist,album,count,rating,len) FROM 'library.csv' WITH DELIMITER ',' CSV;
```

- This command copies data from the `library.csv` file into the `track_raw` table, specifying the columns to be imported and the delimiter used in the CSV file. The `WITH DELIMITER ',' CSV` part indicates that the file is in CSV format and uses a comma as the delimiter between values.
