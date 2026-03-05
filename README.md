# sql-vector-search-api (Pinecone) — Fork & Run Guide

This repo is a **ready-to-run** FastAPI microservice that exposes a single endpoint:

- `POST /v1/search`

It queries **Pinecone** using **metadata filters** (simple JSON) and returns matching records as:

- `id`
- `score`
- `metadata`
- `chunk` (text extracted from metadata)

✅ You can fork this project and run it **without writing code** — only configure environment variables and send requests.

---

## What this service does

### Input (Product Spec)
You send:

- `filters`: a Pinecone metadata filter object (simple JSON)
- Optional:
  - `namespace`: Pinecone namespace override
  - `query_text`: text to generate an embedding and **rank** results semantically
  - `top_k`: how many results to return

### Output
You get a JSON response with:

- a list of matching Pinecone vectors, each with:
  - `id`
  - `score`
  - `metadata`
  - `chunk` (pulled from metadata keys like `chunk`, `text`, `content`, `body`)

> The service **never** returns embeddings.

---

## Default behavior (Important)

### `top_k` default = "all matches"
If `top_k` is **not provided**, the service will try to return **all records that match the filters**.

Because Pinecone requires a `top_k` per query, the implementation usually works like this:
- it paginates/streams through results and aggregates them until exhausted (or a safe cap is reached)

If the repo includes a safety cap (recommended), it will be documented via env var (example: `MAX_RESULTS=5000`).

---

## Project Structure

```text
sql-vector-search-api/
  app/
    main.py
    api/
      routes.py
      schemas.py
    services/
      embedder.py
      search_orchestrator.py
    connections/
      vector_store_base.py
      pinecone_store.py
    core/
      config.py
      logging.py
  requirements.txt
  .env.example
  README.md

## Fork

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

