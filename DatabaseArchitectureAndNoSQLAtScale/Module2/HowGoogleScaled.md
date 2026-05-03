# How Google Scaled Their Operations

---

## Searching Scatter Gather (Marissa Mayer @ Google I/O 2008)

---

### Google Search Request and Response Flow

End User -> Load Balancer -> Mixer -> Google Web Server -> Ads + Web Search (Thousand of backends) -> Mixer -> Load Balancer -> Search Results

During the whole operations query would hit 1000s of machines and at least few datacenters and would collect millions of result in fractions of a seconds.

---

## How Google deploys their hardware (2009) - Container Data Center

---

- 45000 servers in 45 containers housed inside
- Data Center itself went into service in 2005 and supports 10MW of IT equipment load
- Cooling Towers, Power Distribution Units, and other infrastructure
- Better than 99.5% efficiency of transformer

---

## How Search Works (Software)

---

When you do a Google Search - you are not actually searching the web, you are searching Google's index of the web. Or at least as much of the web Google has indexed.

This is done using software program called spiders.
Billions of pages across thousand of machines.

Software searches for all the pages where your search term occurs. Then it ranks them according to more than 200 metrics including `PageRank` and then returns the results to you in fractions of a second.
