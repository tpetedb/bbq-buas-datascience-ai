# BUas Data Science & AI BBQ — Dinner Menu

*(Version 1.0.0 — because semantic versioning also applies to food)*

---

### **Mezze (Streaming pipeline into landing bucket)**

Start with a surprise mezze platter: a rotating selection of dips, pickles, and small bites.
Partitioned evenly across the table to prevent hot spots.
Don’t forget frequent checkpoints to avoid both **data skew** and **hunger-induced downtime**.

---

### **Starters & Dips (Bronze layer metadata)**

**Hummus bil Lahme**
Classic chickpea dataset ingested raw, then transformed with beef embeddings, pine nut tokens, and a drizzle of pomegranate molasses.

**Mtabbal**
Smoky eggplant payload enriched with tahini, lemon, and cumin seeds. Served with a garnish of pomegranate to increase interpretability.

---

### **Bread (Data Shuffling & Load Balancers)**

**Manakish**
Za’atar flatbread — acts like a shuffle key, ensuring fair distribution across all partitions (guests). Caches well, reheats fast.

---

### **Main (The Heavy Compute Layer — Silver/Gold Transformations)**

**Mixed Kebab Selection**
A distributed batch job of skewers (lamb kofta, chicken, beef).
Optimized on a hot cluster (the grill) with parallel processing.
Expect low latency, high throughput, and maybe some spicy outliers.

---

### **To Share (Replicated Storage Layer)**

Flatbreads, herbs, and olive oil — replicated across nodes (tables).
Strong consistency guaranteed: everyone gets a copy.

---

### Extra Notes (Orchestration & Monitoring)

* All jobs tested directly on **prod** (my kitchen). No dev/staging environment available.
* Datasets (ingredients) are **not guaranteed to be balanced** — some variance expected.
* Any **pipeline failures** will be rolled back into dessert.
* Bugs will be served **medium-rare** — retry logic optional.