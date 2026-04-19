# Notes on Relational Database Design in PostgreSQL

---

## Database Design

---

- Database design is an `art form` of its won with particular skills and experience
- Our goal is to avoid the really bad mistakes and design clean and easily understood databases.
- Others may performance tune things later.
- Database design starts with a picture...

---

## Building a Data Model

---

- Drawing a picture of data objects for our application and then figuring out how to represent the objects and their relationships
- **Basic Rule:** Don't put the same string data in twice - use a relationship instead
- When there is one thing in the "real world" there should only be one copy of that thing in the database.
- In a way it is form of compression through connection.

We want to make sure that there is not repetition of data in database. If there is repetition of data then we have to update multiple places when we want to change that data. This can lead to errors and inconsistencies in the database. By using relationships instead of repeating data, we can ensure that there is only one copy of each piece of data in the database, which makes it easier to maintain and update the data. This is a fundamental principle of relational database design and helps to ensure the integrity and consistency of the data.

**Vertical replication of string data is what we don't want to do.**
**Numbers can be replicated because they are cheap to store.**

**Replication is ok and most times preferred in user interface.**

### For each "piece of info"

- Is the column an object or an attribute of another object.
- Once we define objects, we need to define the relationships between those objects.

---

## Keys

---

There are three kinds of keys (which are connection points or identifiers) in a relational database design:

- **Primary Key** - A unique identifier for each record in a table. It ensures that each record can be uniquely identified and is often used as a reference point for relationships between tables. Usually an integer that is automatically generated (like `SERIAL` in PostgreSQL).
- **Logical Key** - What the outside world uses for lookup. For example, an email address can be a logical key for a user because it is unique and can be used to identify the user. Logical keys are often used for enforcing uniqueness of values in a column, but they are not used for joining tables.
- **Foreign Keys** - A field in one table that uniquely identifies a row of another table. It is used to establish and enforce a link between the data in two tables. For example, if we have a `users` table and an `orders` table, the `orders` table might have a foreign key that references the primary key of the `users` table to indicate which user placed each order.

There are some common naming conventions for keys in relational database design. Usually this changes from project to project but here are some common conventions, which are not strict rules but can help with readability and consistency.

- Primary keys are often named `id`.
- Foreign keys will be `<foreign_table_name>_id`. For example, if we have a `users` table and an `orders` table, the foreign key in the `orders` table that references the `users` table might be named `user_id`.

### Primary Key Rules

Best Practices:

- Never use your `logical key` as the `primary key`.
- `Logical Keys` can and do change, albeit slowly
- `Relationships` that are based on matching string fields are less efficient than integers.

---
