# Unesco Heritage Sites Many-to-One

In this assignment you will read some data in comma-separated-values (CSV) format and produce properly normalized tables as specified below. Once you have placed the proper data in the tables, press the button below to check your answer.

---

## Step 1: Create **unesco_raw** table

```sql
DROP TABLE IF EXISTS unesco_raw;
CREATE TABLE unesco_raw (
    name TEXT,
    description TEXT,
    justification TEXT,
    year INTEGER,
    longitude FLOAT,
    latitude FLOAT,
    area_hectares FLOAT,
    category TEXT,
    category_id INTEGER,
    state TEXT,
    state_id INTEGER,
    region TEXT,
    region_id INTEGER,
    iso TEXT,
    iso_id INTEGER
);
```

```sh
pg4e_232debcf0e=> SELECT * FROM unesco_raw;
 name | description | justification | year | longitude | latitude | area_hectares | category | category_id | state | state_id | region | region_id | iso | iso_id
------+-------------+---------------+------+-----------+----------+---------------+----------+-------------+-------+----------+--------+-----------+-----+--------
(0 rows)
```

---

## Step 2: Copy data from 'whc-sites-2018-small.csv' to `unesco_raw` table

```sh
pg4e_232debcf0e=> \copy unesco_raw(name,description,justification,year,longitude,latitude,area_hectares,category,state,region,iso) FROM 'whc-sites-2018-small.csv' WITH DELIMITER ',' CSV HEADER;
COPY 1044
```

- `HEADER` is used to ignore the first line of the csv file which contains column names.
- `\copy` command needs to be in one line.

---

## Step 3: Create the tables necessary for normalization

All tables are in `unesco_tables.sql` file. You can create the tables by running the sql file.

```sh
pg4e_232debcf0e=> \i unesco_tables.sql
```

Some helper queries used are:

```sql
SELECT COUNT(DISTINCT justification) FROM unesco_raw;
```

This for checking how many distinct justifications are there in the `unesco_raw` table.
This can be adjusted for other columns as well.

```sql
SELECT MIN(LENGTH(column_name)), MAX(LENGTH(column_name)) FROM table_name;
```

This for checking the minimum and maximum length of the values in a column. This can be adjusted for other columns as well.

Tables create are:

- `category` table to store distinct categories of heritage sites.
- `state` table to store distinct states of heritage sites.
- `region` table to store distinct regions of heritage sites.
- `iso` table to store distinct iso codes of heritage sites.
- `justification` table to store distinct justifications of heritage sites.

---

## Step 4: Normalize the data

### 1. Copy distinct values of `category` from `unesco_raw` to `category` table

```sql
INSERT INTO category (name) SELECT DISTINCT category FROM unesco_raw ORDER BY category;
```

### 2. Insert corresponding `id` from `category` table to `category_id` column in `unesco_raw` table

```sql
UPDATE unesco_raw SET category_id = (SELECT category.id FROM category WHERE category.name = unesco_raw.category);
```

### 3. Copy distinct values of `justification` from `unesco_raw` to `justification` table

```sql
INSERT INTO justification (reason) SELECT DISTINCT justification FROM unesco_raw ORDER BY justification;
```

### 4. Insert corresponding `id` from `justification` table to `justification_id` column in `unesco_raw` table

We need to add `justification_id` column to `unesco_raw` table before running the update query.

```sql
ALTER TABLE unesco_raw ADD COLUMN justification_id INTEGER;
```

```sql
UPDATE unesco_raw SET justification_id = (SELECT justification.id FROM justification WHERE justification.reason = unesco_raw.justification);
```

### 5. Repeat the above steps for `state`, `region` and `iso` tables

```sql
INSERT INTO state (name) SELECT DISTINCT state FROM unesco_raw ORDER BY state;
INSERT INTO region (name) SELECT DISTINCT region FROM unesco_raw ORDER BY region;
INSERT INTO iso (code) SELECT DISTINCT iso FROM unesco_raw ORDER BY iso;
```

```sql
UPDATE unesco_raw SET state_id = (SELECT state.id FROM state WHERE state.name = unesco_raw.state);
UPDATE unesco_raw SET region_id = (SELECT region.id FROM region WHERE region.name = unesco_raw.region);
UPDATE unesco_raw SET iso_id = (SELECT iso.id FROM iso WHERE iso.name = unesco_raw.iso);
```

### 6. Insert data from `unesco_raw` to `unesco` table

```sql
INSERT INTO unesco (name, description, year, longitude, latitude, area_hectares, category_id, justification_id, state_id, region_id, iso_id) SELECT name, description, year, longitude, latitude, area_hectares, category_id, justification_id, state_id, region_id, iso_id FROM unesco_raw;
```
