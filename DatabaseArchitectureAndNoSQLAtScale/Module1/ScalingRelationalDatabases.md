# Notes on Scaling Relational Databases

---

## Why did we look at BASE at all?

---

Key is that, it was difficult to scale relational databases. Only way to scale relational database was to scale vertically, which is expensive and has limits.

## Vertical Scaling

- More disk drives or disk arrays / RAID
- More processors
- More memory
- Switch from spinning to solid state drives
  - Modern SSD drives have scatter / gather.
- Has been solidly successful over the years
- But has limits and is expensive

---

## Tuning Relational Databases

---

Relational databases are good by default up to a certain point around (100K to 1M rows).
So we need to tune the database to get the best performance out of it for scaled systems. We need to do things like:

- **Read only replicas**: We can have one master database that handles all the writes, and multiple read replicas that handle all the reads. This way we can scale the reads horizontally. Base like read system.
- **Multi-Master**: We can have multiple master databases which co-ordinate well enough that we have consistency. Usually its not a good solution, since it is difficult to co-ordinate between multiple master databases.
- **Multiple Store Types**: We have different store types for different of data. We can store in a relational database where the blob (images/files) are stored in a file system. And store the blob in actually a file system.
- **Multi-Tenant / "Pretend Cloud"**: Bunch of application code for each application we have a separate database. This way we can scale horizontally by adding more databases as we add more applications.
