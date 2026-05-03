# Notes on To SQL or to NoSQL

---

## Why NoSQL?

---

Some normalization rules we learned are a bit flexible.

- **Do not replicate string data**: This is true for 95% of the time, but there are cases due to your application requirements you may very well forced to replicate data. But a decision needs to be made on a case by case basis, and you need to understand database normalization rules to make an informed decision.

**Now a days there are lots of evolving requirements for a database which needs to be highly available and scalable.** All these requirements are encapsulated in NoSQL.

---

## SQL or NoSQL?

---

### A better question

This question is not a good idea, because SQL is a syntax. And NoSQL file storage was considered previously and discarded as less optimal for a lot of use cases. So the question is not SQL or NoSQL, but rather **relational** or **non-relational**.
**Rows and Columns** _Vs_ **Documents, Keys and Values**

### Best question

The best question in this context should be **ACID** _Vs_ **BASE**. ACID stands for Atomicity, Consistency, Isolation and Durability. BASE stands for Basically Available, Soft state and Eventually consistent.

### ACID

**ACID** basically makes sure that at one moment of time every observer sees the same data

- Atomicity: All or nothing, either all the operations in a transaction are executed or none of them are.
- Consistency: The database is in a consistent state before and after the transaction.
- Isolation: The operations in a transaction are isolated from other transactions, meaning that they do not interfere with each other.
- Durability: Once a transaction is committed, it is permanent and will survive any subsequent failures.

### BASE

**BASE** is a more relaxed approach to data consistency. Eventual consistency is the goal here.

- Basically Available: The system is designed to be available at all times, even in the face of failures.
- Soft state: The state of the system may change over time, even without input, due to eventual consistency.
- Eventually consistent: The system will eventually become consistent, but it may not be consistent at all times.

### Example of ACID vs BASE

**CASE**: Data currently is `x=42`. We have two simultaneous operations: `x=10` and `x=20`.

### In case of ACID

- Both operations will be executed in isolation, meaning that one operation will be executed before the other. So either `x=10` or `x=20` will be the final value of `x`, but not both.

### In case of BASE

- In this case, there will be multiple copy of `x=42` on different server (for high scalability)
- Suppose there are 3 servers numbered 1, 2, 3.
- At time `0`, all servers have `x=42@0`.
- At time `1`, `x=10` is executed on server 1, so server 1 has `x=10@1`. Server 2 and 3 still have `x=42@0`.
- At this time, multiple observers will see different values of `x` depending on which server they are connected to. Some will see `x=10`, while others will see `x=42`. This is the inconsistent moment.
- At time `2`, `x=20` is executed on server 2, so server 2 has `x=20@2`. Server 1 still has `x=10@1` and server 3 still has `x=42@0`.
- Now, observers can see `x=10`, `x=20` or `x=42` depending on which server they are connected to. This is still the inconsistent moment.
- Now at time 3, servers will start syncing, and server1 will tell at time 1, x was updated to 10. But the server 2 will see that, and see that it has time 2 update to 20, so it will throw away server 1's update. And server 3 will see both updates and will keep the latest one, which is `x=20@2`. So at time 3, all servers will have `x=20@2`. Server 1 will also see that latest update is `x=20@2`, so it will update its value to `x=20@2`. This is the eventually consistent moment.

---

## Database Software

---

### ACID (Atomic)

- Oracle
- PostgreSQL
- MySQL
- SQLite
- SQLServer

### BASE (Eventual)

- MongoDB
- Cassandra
- DynamoDB
- BigTable

---

## Compromises

---

| **ACID (Atomic)**           | **BASE (Eventual)**                  |
| --------------------------- | ------------------------------------ |
| SERIAL INTEGER Keys         | GUIDs - Globally Unique IDs          |
| Transactions                | Design for stale data in application |
| UNIQUE Constraints          | Application post-check and resolve   |
| "One perfect SQL statement" | Retrieve and throw away              |
