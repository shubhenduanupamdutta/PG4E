# Notes on Second Generation Cloud Application

---

First Generation - Google, Gmail
Second Generation - Facebook, Twitter

---

## Facebook is More Challenging

---

- Friend list - edit / app / drop / list
- Privacy
- Everyone sees a very different view
- Everyone searches a different corpus
- Data locking for predictable update is replaced by data sharding and replication
- Migrate data "to be close" to the viewer

---

## Problems to solve

---

- Clever non-locking solutions to distribution
  - GUIDs for primary keys
  - Hashing / Sharding for predictable data placement / lookup
- Some central control - mostly "what is where"
- Perhaps use one or more RDBMS for taking money or new accounts.
