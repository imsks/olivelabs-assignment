Problem 1 — Full-Stack NLQ App (Add a New Feature Without Breaking Flow)
Goal
Build a small full-stack app that lets business users query a relational dataset in natural language and see results as a table or chart. Then add query explainability without breaking existing NLQ → SQL → Viz flows.
Tech Stack (suggested)
UI: React + TypeScript, Vite/Next.js, Charting (Recharts or ECharts), Zustand/Redux for state.

Backend: Python (FastAPI), Pydantic, SQLAlchemy, Celery (optional for async), uvicorn.

DB: Postgres (with sample schema: orders, customers, products).

Search/Vector (optional): pgvector / SQLite + FAISS for schema grounding.

Auth: JWT (Auth0 or simple in-app JWT for exercise).

Infra (mock acceptable): Docker Compose, pytest, GitHub Actions (lint + test).

Minimal Data Model
orders(order_id, customer_id, product_id, order_date, quantity, unit_price, region)

customers(customer_id, name, segment, country)

products(product_id, product_line, category)

Derived: revenue = quantity \* unit_price

Required Features
NLQ → SQL

Convert a prompt like “revenue by region in Q2 2024” into a safe SQL query over the above schema.

Must validate columns/tables (whitelist) and reject dangerous SQL.

Results + Visualization

Results shown as table.

If query produces groupable numeric series, also show chart (bar/line).

Toggle between views.

Conversational Refinement

Follow-up like “break it down by product line” should carry prior context.

Maintain turn-level state (server session or client conversation id).

New Feature to Add (without breaking flow)
Query Explainability

Show a short, human-readable “how I built the SQL” + a structured provenance object:

{
"filters": ["order_date in Q2 2024"],
"groupBy": ["region"],
"aggregates": ["sum(revenue)"],
"sourceTables": ["orders", "products"]
}

Existing URLs and API responses for results must remain backward compatible.

API Surface (proposed, FastAPI)
POST /api/nlq/parse
Body: { "prompt": "revenue by region in Q2 2024", "conversation_id": "opt" }
Resp: { "sql": "...", "warnings": [], "explain": { ... }, "conversation_id": "..." }

POST /api/nlq/execute
Body: { "sql": "SELECT ...", "result_format": "table|series" }
Resp: { "columns": [...], "rows": [[...]], "inferred_chart": "bar|line|null" }

POST /api/nlq/query // convenience: parse+execute
Body: { "prompt": "...", "conversation_id": "opt" }
Resp: {
"columns": [...], "rows": [[...]],
"inferred_chart": "bar|line|null",
"explain": { "filters": [...], "groupBy": [...], "aggregates": [...], "sourceTables": [...] },
"sql": "..."
}

GET /api/schema/describe
Resp: { "tables": [{ "name":"orders", "columns":[{"name":"order_id","type":"int"}, ...]}] }

POST /api/conversation/refine
Body: { "conversation_id": "abc", "followup": "break it down by product line" }
Resp: same shape as /api/nlq/query

Internal Modules (Python)
schema_registry.py: whitelist tables/columns; human labels.

nlq_parser.py: turns prompt + registry into SQL AST, then SQL string.

safety.py: denylist keywords, enforce SELECT-only, LIMIT caps.

viz_inference.py: inspects shape to propose chart type.

explain_builder.py: emits explainability object from AST.

sessions.py: conversation state.

UI Flows (React)
Query Panel (prompt input, history chips).

Results View (table + chart tabs).

Explainability Drawer (collapsible panel with “how SQL was formed”).

Schema Tooltip (hover to see field descriptions).

Back-Compat Constraints (what you evaluate)
/api/nlq/query still returns the same columns/rows/inferred_chart/sql keys; explain is additive.

No change needed in the “Results View” to keep working (explain panel can attach later).

Acceptance Tests
NLQ produces correct SQL for: filter + group + aggregate + order + limit.

Follow-up modifies previous query correctly (adds GROUP BY product_line).

SQL safety rejects DROP, INSERT, cross-db refs, or unknown columns.

Explain object accurately mirrors produced SQL.

Chart inference works for groupable numeric outputs; disabled otherwise.

Stretch (optional, nice signals)
Guardrails: unit tests for parser; golden test prompts.

Caching: memoize parse results by normalized prompt + schema hash.

Cost-aware: knob to switch between LLM and rule-based parser for simple intents.
