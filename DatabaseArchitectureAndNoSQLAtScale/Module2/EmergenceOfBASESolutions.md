# Note on Emergency of BASE Solutions i.e. NoSQL Databases

---

## The basic principles of BASE DBMS

---

- Everything is distributes - fast network
- No locks (`*`)
- Lots of fast / small memory CPUs
- Lots of disks
- Indexes follow data shards
- Document not rows / columns
- Schema on read - not schema on write (`*`)

---

## JSON Ascending

---

- JSON is a great way to represent / move / store structured data.
- Fast parsers in every programming language.
- Easily compressed to save storage and transfer.

---

## Open Source NoSQL Databases

---

- CouchDB (2008)
- Cluster Of Unreliable Commodity Hardware Database
- MongoDB (2009)
- Distributed JSON storage
- Cassandra (2008)
  - From Facebook
  - Also apache Hadoop - Map / Reduce
- ElasticSearch (2010)
  - Initially full text search Apache Lucene
  - Evolved into JSON database

---

## Proprietary / Software as a Service (SASS) NoSQL Databases

---

- Amazon DynamoDB
  - Backed by Amazon Catalogue
- Google BigTable
  - Backed by Google
- Azure Table Storage

---

## Be like FaceBook - Make Money

---

- Emergency of client-side applications
  - Backbone, Angular, React, Vue ...
- Emergence of JavaScript in the server
  - node.js - great at async / microservices
- NoSQL Databases
  - Distributed, Scalable, inexpensive resources
- Lots of startups / fresh ground up development

---

## Case Study: Vericite

---

- Startup founded in 2014 - expected 100 TB
  - Cloud / multi-tenant / document based
- Used MySQL for PoC - Did not want to shard
- Built on Cassandra and "owned hardware"
- Cassandra fell down at scale - consultant
- Switched to Amazon Dynamo DB
  - Works - expensive but cheaper than consultants
- NoSQL database competed against larger firm using custom storage on physical hardware.
