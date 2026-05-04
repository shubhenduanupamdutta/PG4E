# Notes on Exploring CRUD in DenoKV Using KVAdmin

---

## Deno has no official admin tool (for now)

---

- No PgAdmin, no DBeaver, no PHPMyAdmin
- Not even a command line pg or mysql client
- All you get is a way to view KV data in the dashboard (for now)

---

## A Simple Deno + Hono Web Server

---

```javascript
import { Hono } from "https://deno.land/x/hono@v3.4.1/mod.ts";
const app = new Hono();

app.get("/hello", async (c) => {
	const result = { answer: "world" };
	return c.json(result);
});

Deno.serve(app.fetch);
```

---

## Deno KV Connection

---

```javascript
import { Hono } from "https://deno.land/x/hono@v3.4.1/mod.ts";
const app = new Hono();
const kv = await Deno.openKv();

// Get a record by key
// https://kv-admin-api.pg4e.com/kv/get/books/Hamlet?token=42

app.get("/kv/get/:key{.*}", async (c) => {
	checkToken(c);
	const key = c.req.param("key");
	const result = await kv.get(key.split("/")); // ['books', 'Hamlet']
	return c.json(result);
});

// ...

Deno.serve(app.fetch);
```
