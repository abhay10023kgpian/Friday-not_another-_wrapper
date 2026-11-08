# Friday — AI-Powered E-Commerce Assistant

An intelligent shopping assistant backend that understands natural language product queries, answers policy questions from company documents, and keeps search results fresh in real-time — all powered by a multi-strategy LangGraph agent pipeline.

---

## Problems Solved

### 1. Vector Search Fails on Structured Queries

**Problem:** A customer asks *"show me shoes under $80"* — vector similarity search returns semantically similar product descriptions, but has no concept of numeric filtering. Results include $190 shoes because the word "price" is semantically close. The same failure occurs for size filtering, brand-exact matching, and sorting by price.

**Solution:** Built a **3-way intent router** that classifies every query into one of three strategies before execution:

| Intent | Route | Example |
|---|---|---|
| Structured filter/sort | **Text-to-SQL** → PostgreSQL | *"cheapest Nike shoes in size 10"* |
| Semantic/descriptive | **Hybrid vector search** → Elasticsearch | *"comfortable shoes for marathon training"* |
| General / chitchat | **Direct LLM** (no retrieval) | *"how do I clean suede shoes?"* |

The LLM generates safe, read-only SQL (`SELECT` only) from natural language — turning vague filter requests into precise database queries against 215+ products.

**Result:** 88% routing accuracy and 93% SQL execution success rate on a 50-query evaluation set.

---

### 2. Stale Search Results After Catalog Updates

**Problem:** When a product is added, updated, or removed in the PostgreSQL catalog, the Elasticsearch vector index still serves old data. Traditional approach: run a batch re-indexing job manually or on a cron — introducing minutes-to-hours of stale results and operational overhead.

**Solution:** Implemented a **real-time CDC (Change Data Capture) pipeline**:

```
PostgreSQL (WAL) → Debezium → Kafka → Python Consumer → Elasticsearch
```

Debezium reads the Postgres write-ahead log, publishes change events to Kafka, and a Python consumer automatically embeds and indexes the changed products into Elasticsearch — no polling, no cron jobs, no manual triggers.

**Result:** Product catalog changes are reflected in search results in **<5 seconds**, with zero manual re-indexing.

---

### 3. Full-Table Re-Indexing on Single Row Updates

**Problem:** Even with CDC detecting individual row changes, a naive approach would re-embed and re-index the entire product table on every update — turning an O(1) database change into an O(n) embedding operation. At 215+ products with embedding API calls, this wastes compute and money on every single product edit.

**Solution:** Every product document is indexed with its **`product_id` as the Elasticsearch document ID**. When a CDC event arrives for a specific product:

1. The consumer receives only the changed row (not the full table)
2. Re-embeds only that single product's content
3. Upserts into Elasticsearch by `product_id` — overwriting only that one document

This makes every update an **O(1) operation** regardless of catalog size — one row changed = one embedding call = one index write.

**Result:** Single-product updates cost **1 embedding API call** instead of 215+, reducing per-update embedding costs by **~99.5%**.

---

### 4. Retrieved Chunks Are Mostly Noise

**Problem:** Vector search returns the top-k most similar chunks, but "similar" ≠ "relevant." For a query like *"Nike shoes in size 10"*, the retriever might return chunks about Adidas shoes (similar embedding space), company policy paragraphs mentioning "shoes," or product descriptions for the wrong size. Passing all this noise to the LLM dilutes answer quality and wastes tokens.

**Solution:** Added an **LLM-as-judge relevance grading step** between retrieval and generation. Each retrieved chunk is individually evaluated for relevance to the specific query using structured output. Only chunks that pass the relevance check are included in the generation context.

**Result:** Filters out **~55% of irrelevant chunks** before generation, reducing unnecessary context passed to the LLM and improving answer grounding.

---

### 5. Every Query Hits the Full Retrieval Pipeline

**Problem:** Simple questions like *"hi"*, *"how do I clean shoes?"*, or *"thanks!"* don't need any retrieval — but a naive pipeline sends every query through embedding → vector search → relevance grading → generation. This wastes embedding API calls, Elasticsearch queries, and multiple LLM calls per query that could be answered directly.

**Solution:** The 3-way router (from Problem #1) identifies queries that can be answered from the LLM's general knowledge and routes them **directly to generation**, bypassing the entire retrieval pipeline.

**Result:** **~40% of queries** skip retrieval entirely, reducing average per-query cost (fewer API calls) and improving response latency for non-retrieval questions.

---

## Architecture

```
                          ┌──────────────────────────────────────────────┐
                          │           LangGraph Agent Pipeline           │
                          │                                              │
User Query ──→  ┌─────────────────┐                                     │
                │  Route Query    │                                     │
                │  (3-way LLM)    │                                     │
                └────────┬────────┘                                     │
                         │                                              │
            ┌────────────┼────────────┐                                 │
            ▼            ▼            ▼                                 │
    ┌──────────────┐ ┌──────────┐ ┌──────────────┐                     │
    │ Text-to-SQL  │ │ Hybrid   │ │   Direct     │                     │
    │ (PostgreSQL) │ │ Search   │ │   LLM        │                     │
    └──────┬───────┘ │(Elastic) │ └──────┬───────┘                     │
           │         └────┬─────┘        │                             │
           │              ▼              │                             │
           │     ┌──────────────┐        │                             │
           │     │  Relevance   │        │                             │
           │     │  Grading     │        │                             │
           │     └──────┬───────┘        │                             │
           ▼            ▼                ▼                             │
    ┌────────────────────────────────────────────┐                     │
    │          Generate from Context             │                     │
    └────────────────────┬───────────────────────┘                     │
                         │                                              │
                         ▼                                              │
                      Response                                          │
                          └──────────────────────────────────────────────┘


            ┌──────────────────────────────────────────┐
            │       Real-Time CDC Pipeline              │
            │                                          │
PostgreSQL ──→ Debezium ──→ Kafka ──→ Consumer ──→ Elasticsearch
  (WAL)        (CDC)       (Events)   (Embed &      (Vector Index)
                                       Upsert)
            └──────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph (StateGraph) |
| LLM | Groq (GPT-OSS-120B) |
| Embeddings | OpenAI text-embedding-3-small (512-dim) |
| Vector Search | Elasticsearch 8.15 (hybrid: dense + BM25) |
| Database | PostgreSQL 17, SQLAlchemy |
| CDC | Debezium 3.3, Kafka (KRaft mode) |
| Language | Python 3.11+ |

## Project Structure

```
backend/
├── src/
│   ├── retrieval/
│   │   ├── hybrid_retriever.py     # LangGraph pipeline (3-way routing)
│   │   ├── vector_store.py         # Elasticsearch store setup
│   │   ├── embed.py                # Company document indexing
│   │   ├── embed_products.py       # Product embedding (chunk-ID upsert)
│   │   ├── kafka_embedder.py       # CDC consumer → real-time embedding
│   │   └── hybrid_search.py        # Standalone search utility
│   ├── infrastructure/
│   │   ├── database/postgres/
│   │   │   ├── connections.py      # SQLAlchemy engine & session
│   │   │   ├── init_db.py          # Run migrations
│   │   │   ├── insert.py           # Seed product data
│   │   │   └── migrations/         # SQL migration files
│   │   ├── kafka/
│   │   │   ├── consumer.py         # Generic Kafka consumer
│   │   │   └── producer.py         # Generic Kafka producer
│   │   └── debezium/
│   │       └── postgres-connector.json
│   └── data/                       # Company PDFs for knowledge base
├── tests/
│   ├── eval/
│   │   ├── test_queries.json       # 50-query evaluation dataset
│   │   └── results.json            # Evaluation output
│   └── run_eval.py                 # Automated eval script
├── docker-compose.yaml             # Elasticsearch, Postgres, Kafka, Debezium
└── pyproject.toml
```

## Setup

```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Create virtual environment
python -m venv myvenv
myvenv\Scripts\activate

# 3. Install dependencies
pip install -r src/retrieval/requirements.txt
pip install -r src/infrastructure/requirements.txt

# 4. Set environment variables (.env files)
# See src/retrieval/.env and src/infrastructure/.env

# 5. Initialize database & seed products
python src/infrastructure/database/postgres/init_db.py
python src/infrastructure/database/postgres/insert.py

# 6. Index documents into Elasticsearch
python src/retrieval/embed.py
python src/retrieval/embed_products.py

# 7. (Optional) Start CDC consumer for real-time sync
python src/retrieval/kafka_embedder.py

# 8. Run the chatbot
python src/retrieval/hybrid_retriever.py
```

## Evaluation

```bash
python tests/run_eval.py
```

Runs 50 test queries across 4 categories (product search, company knowledge, general knowledge, chitchat) and measures:

- **Routing accuracy** — did the router pick the right strategy?
- **Retrieval reduction** — % of queries that skipped retrieval entirely
- **SQL execution success** — % of generated SQL queries that returned valid results
- **Latency** — p50 and p95 response times

