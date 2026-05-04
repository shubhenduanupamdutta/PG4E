# Notes on Deno and DenoKV

---

## Online Resources

---

- [DenoKV Quick Start](https://docs.deno.com/deploy/kv/)
- [Deno Deploy Hosting](https://dash.deno.com/)
- [KV Admin Install Instructions](https://github.com/csev/deno-kv-admin/blob/main/README.md)

### Routing Details

- **Production**: _https://`{app-slug}`.shubhenduanupamdutta.deno.net_
- **Branch**: _https://`{app-slug}`--`{branch-name}`.shubhenduanupamdutta.deno.net_
- **Preview**: _https://`{app-slug}`--`{revision}`.shubhenduanupamdutta.deno.net_

### Deno Deploy

- [Console](https://console.deno.com/shubhenduanupamdutta)

---

## History of Deno

---

- Emerged from the NodeJS server project
  - JavaScript server for web applications
  - Node was founded in 2009 by Ryan Dahl
- Ryan Dahl founded Deno (Node spelled backwards) in 2018
  - Fresh start with a decade of experience with Node
  - Some _Node_ things just **happened** and became required / core and that limited innovation

---

## Node Pain Points

---

- JavaScript / TypeScript battle
  - Hope was that TypeScript as pre-processor would be temporary and JavaScript would be TS
- Node started as a technology base
  - Not opinionated
  - Extended with a series of modules that were maintained independently
- Dependency management / `npm`
- Maintaining / Improving Node was difficult

---

## Evolving Distributed Architectures

---

- Why serve static assets from one server in Ohio in the USA?
  - Slow and bandwidth is expensive
- Edge caching of static assets
  - Akami (1998), Amazon CloudFront (2010), Cloudflare (2010), Fastly (2011), Netlify (2014)

---

## CloudFlare is great for Content

---

- **Free** / Inexpensive edge caching / serving of static assets
- No cost Distributed Denial of Service (DDoS) protection
- The actual www.py4e.com application runs on one EC2 server in Amazon backed by an Amazon Auto-scale MySQL Aurora Database
- The PY4E server _only_ accepts network connections from CloudFlare servers

### CloudFlare provides in free tier

- Caching of static assets
- DDoS protection
- SSL / TLS termination
- Distributed DNS
- It also added `JavaScript Workers` in 2018

---

## CloudFlare Workers - Dr. Chuck's Concerns

---

- It feels **emergent** - I don't have time to rewrite my app every year
- I have no experience how costs might scale for a system like _www.py4e.com_
- First, I would experiment with a small part of a production application

---

## Enter Deno - Modern NodeJS

---

- Deno is a JavaScript based web server
  - Standard Library - lots of dependencies for basic JavaScript capabilities (like Cryptography) are part of each Deno release
  - Deno gives a choice of JavaScript and TypeScript out of the box
- Kind of like **Django** (Vs. _Flask_) - **with batteries included** and **opinionated** - but for JavaScript
- Still emerging (Deno 2.0 - October 2024)

---

## Deno - More than a server

---

- **Deno Deploy** - Distributed Hosting
  - Commercial service from _deno.com_
  - Free for low volume developer sites (\*\*\*)
  - Open source if you want to use your own resources
- **Deno KV (Key Value)** a built-in distributed JSON database with every Deploy instance
- **Deno KV Watch** - Publish / Subscribe / Notifications worldwide - Like redis

---

## Deno KV Peer Products

---

- CloudFlare Workers KV
- Upstash Redis
- Amazon DynamoDB
- Google Firestore / Firebase
- Folks Dr. Chuck's know who use these at scale say, **Deep Pockets**

---

## Why Deno has potential (for me)

---

- So much built in
  - Deno + Standard JS library
  - Deno KV
  - Deno KV Watch
- **Free Deno Deploy** - Great for teaching
- **Distributed Deno KV** and **KV Watch** built in
- Low cost distributed notifications are important in educational applications
