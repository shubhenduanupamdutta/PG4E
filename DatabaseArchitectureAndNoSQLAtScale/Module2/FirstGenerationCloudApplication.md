# Notes on First Generation Cloud Application

---

## Google Cloud Did Not Use RDBMS

---

- They also chose applications that did not require transactions
  - Everything was free - or "the first ~100 Mb was free"
  - Updates were widely distributed - even to email
  - All these applications didn't need atomic consistency.
- Early Google Applications were not Facebook or Twitter
- They could use cleverly names files and folders and sharding/hashing across servers.

---

## Conclusions From Youtube Videos

---

### Melissa Mayer's talk at Google I/O 2008

- It is not always about how fast. Sometime slightly delay is ok, if it doesn't affect user experience.
- Data is flowing through multiple servers very very quickly. Partitioning querying servers and data across multiple servers is the key to scale.
- Google used mixer to aggregate the results from multiple servers and then return the results to the user.

### Container Data Center

- Nothing special but backups, cooling and power distribution units are important for scale.
- Not wasting energy.
- Lifecycle of older computers.
- Data is replicated multiple times for durability and availability.

### How Search Works (Software)

- In downtime of a server, web is indexed and ranked.

---

## Amazon Web Services (AWS)

---

- Amazon launched AWS: first generation cloud application.
- CPU and storage were cheap, but speed of storage and memory was expensive.
- You can buy lot of storage and CPU very cheaply.
- Developer start renting out CPU and storage from Amazon, and then we need to redesign our applications to work with the cloud, which is slow and has less memory.
- These clusters are also called "carpet clusters"

---

## Efficient Use of "Carpet Clusters"

---

- Spread data out across many systems.
- Scatter the query to all the systems.
- Gather the results
- (a.k.a Map-reduce)
- A single query might be 1-2 seconds.
- many queries could be "in flight" at the same time (need a fast network)
- You might just run a RDBMS on each node and shard.
