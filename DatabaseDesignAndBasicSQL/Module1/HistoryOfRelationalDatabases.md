# Notes on History of Relational Databases

---

## Before Databases

---

It is not so bad to read a file, (even while it was on tape), but it is a linear thing. So there was a lot of access time.
Idea was that, we would sort the data in an old tape. And then we would sort all the transaction punch card. And then we merge the two together around midnight. This was called `Sequential Master Update`.

---

## Random Access

---

Today we have lot faster drive, which also has random access. So for all intent and purposes, we can get to any point of the memory in a very short amount of time. How do we take advantage of that? In this case `Sequential Master Update` will not utilize the random access. So we need to have a different way of doing things. We need to have a way to get to the data that we want to get to without having to read through all the data that we don't want to get to.

In the 60s and 70s, lot of companies started building `Relational Databases` to solve this problem. The relational database you can properly bounce around the data to quickly get to needed data. It is grounded in mathematics, but it took a lot of time to software to catchup.

There were lot of vendors at the time. For vendor lock-in reasons, most companies would only provide support for one database and hardware.

Some point there was a need for standardization. So NIST (National Institute of Standards and Technology) started a project to standardize database access. They came up with a common interface language called `SQL` (Structured Query Language). It was a big deal at the time. It was a big deal because it meant that you could write your application in SQL and then you could run it on any database that supported SQL. So you could write your application in SQL and then you could run it on Oracle, or you could run it on MySQL, or you could run it on Postgres, or you could run it on SQL Server. And so that was a big deal because it meant that you were not locked into a particular database vendor.

### Procedural and Non-Procedural Languages

- **Procedural Language**: All the instructions are given to the computer in a specific order. You have to tell the computer what to do and how to do it. You have to tell the computer how to get to the data that you want to get to. You have to tell the computer how to process the data that you want to process. You have to tell the computer how to output the data that you want to output.

- **Non-Procedural Language**: You just tell the computer what you want to get to, what you want to process, and what you want to output. You don't have to tell the computer how to get to the data that you want to get to. You don't have to tell the computer how to process the data that you want to process. You don't have to tell the computer how to output the data that you want to output. `SQL` is a non-procedural language, you tell computer what you want and SQL internally optimizes your query to get the data in most efficient possible way.

---

## CRUD

---

Critical core part of any SQL queries are `CRUD` operations. `CRUD` stands for Create, Read, Update, and Delete. These are the four basic operations that you can perform on a database. You can create a new record in the database, you can read a record from the database, you can update a record in the database, and you can delete a record from the database. These are the four basic operations that you can perform on a database. And SQL provides a way to perform these operations on a database.

---

## Terminology

---

- **Database**: Contains one or more tables. It is a collection of data that is organized in a specific way. It is a collection of tables that are related to each other in some way.
- **Table or Relation**: A collection of rows and columns. Contains tuples and attributes.
- **Tuple (or Row)**: A single record in a table. A set of fields which generally represents an "object" like a person or music track.
- **Attribute (or Column)**: One of possibly many elements of data corresponding to the object represented by the row.

**Data is modeled as relation and connection. The relation is the table and the connection is the relationship between the tables.**

- **Schema**: The structure of the database. What Table (Relations), columns (Attributes) their datatype and relationship between tables. It is the blueprint of the database. It is the structure of the database. It is the way that the data is organized in the database. It is the way that the data is related to each other in the database.

---

## Common Database Systems

---

### Major Database Management Systems in Wide use

- `SqlServer` (Microsoft)
- `MySQL` - Fast and scalable - commercial open source
- `Oracle` - Fast and scalable - commercial, but it is very hard to maintain and it is very expensive.
- `PostgreSQL` - Open source, highly extensible, supports advanced data types and performance optimization features.
- `SQLite` - Open source, embedded, serverless, self-contained, zero-configuration, transactional SQL database engine. It is a very small and lightweight database that is used in many applications.

We will be using `PostgreSQL` in this course. It is a very powerful and popular database that is used in many applications. It is a very good choice for learning SQL because it is open source, it is highly extensible, it supports advanced data types and performance optimization features, and it has a large and active community.
