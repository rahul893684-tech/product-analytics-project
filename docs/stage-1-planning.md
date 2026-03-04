# Project: Product Analytics & User Behavior Analysis

## 1. Business problem
We want to build an end-to-end, reproducible Product Analytics pipeline that ingests event-level data, models it into an analytics-friendly star schema, and delivers SQL + Python analyses and dashboard-ready artifacts to answer:
- Where do users drop out in the activation funnel?
- How long do users retain and how does retention change by signup cohort?
- Which segments of users are highest value and most engaged?

This project is targeted to a product/PM/data team that needs a reproducible analytics repo they can run locally or in CI.

## 2. Measurable KPIs
- Funnel conversion rates (signup → activation → purchase) — target: compute exact conversion %.
- 30-day retention by signup cohort (cohort-month vs retention %) — target: retention table CSV.
- Daily Active Users (DAU) and New Users per day.
- Average Revenue Per User (ARPU) and % users generating revenue.
- Median session length and sessions per user.
- Churn (30-day inactivity) and simple LTV approximation.

## 3. Chosen SQL dialect
- **PostgreSQL** (all SQL in repo will use Postgres syntax).

## 4. Architecture (ASCII)

[Raw events CSV or generator]
|
v
data/download_data.sh (or generate_data.py)
|
v
Postgres (raw_events) <-- COPY \copy from CSV
|
ETL / cleaning.py
|
v
Cleaned CSVs -> staging tables (data/cleaned/.csv)
|
v
SQL Modeling (sql/schema.sql) -> fact_events + dim_users + dim_date
|
v
Analytical SQL Queries (sql/queries/.sql) -> CSV exports (\copy)
|
v
Python analysis (python/analysis.ipynb) -> plots to images/, report.md
|
v
Dashboard (Power BI / Tableau) using exports or direct DB connection


## 5. Tech stack
- PostgreSQL (>=12 recommended)
- Python 3.10+  
  - pandas, numpy, sqlalchemy, psycopg2-binary, scikit-learn, matplotlib
- Docker (optional) + simple `Dockerfile` provided later
- Git (branching per stage)
- Power BI Desktop or Tableau Desktop (dashboard instructions provided in later stage)
- CLI: psql, curl/wget, gh (optional)

## 6. Expected outputs (files & artifacts)
- `data/events.csv` (>= 200,000 rows)
- Postgres tables: `fact_events`, `dim_users`, `dim_date`
- SQL exports: funnel CSV, cohort retention CSV, segmentation CSV
- Python outputs: retention curve PNG, segmentation summary PNG saved to `images/`
- Dashboard guide + screenshots (`dashboard/README.md`, `images/*.png`)
- `README.md` (root) summarizing run steps and findings
- `resume_bullets.md` (3–5 bullets)

## 7. Acceptance criteria (project-level)
These map to deliverable acceptance:
1. **Data volume**: event-level dataset available with **>= 200,000 rows**.
2. **Funnel**: A SQL script `sql/queries/funnel.sql` that outputs conversion numbers and final conversion percentage (single-row or single-result set with stages and conversion %) using CTEs/window functions.
3. **Cohorts**: `sql/queries/cohort.sql` that produces and saves a cohort retention table (signup cohort month × retention%) as CSV.
4. **Python analysis**: `python/analysis.ipynb` (or .py) with code that loads SQL outputs (or reads from DB), produces at least:
   - one retention curve plot saved under `images/` (PNG)
   - one segmentation summary (kmeans or rule-based) saved under `images/`
5. **Dashboard**: `dashboard/README.md` describing exact steps to reproduce funnel, cohort heatmap, retention line, and segment visualizations in Power BI or Tableau.
6. **Reproducibility**: Exact commands to generate/download data, load to Postgres, run SQL queries, and run Python analysis are provided in `README.md`.
7. **Git hygiene**: Branch-per-stage workflow and example commits included.

## 8. Risks & mitigations
- Risk: dataset too small or unrealistic. Mitigation: include robust synthetic generator with realistic distributions and parameter to scale up rows.
- Risk: SQL dialect differences. Mitigation: use only Postgres features (+ document versions).
- Risk: user environment differences. Mitigation: provide Dockerfile and python `requirements.txt`.

## 9. Success metrics for repository (how reviewers will verify)
- Run the `data/download_data.sh` (or generate script) to create `data/events.csv` with >=200k rows.
- Run `psql` COPY to load raw events; run SQL scripts to create and populate star schema.
- Execute `sql/queries/funnel.sql` and validate a single-row result with stage conversion numbers.
- Run Python notebook/script to generate PNGs in `images/`.
- Open `dashboard/README.md` to reproduce visuals in Power BI or Tableau.

## 10. Next steps (stage mapping)
- Stage 2 — Data generation & ingestion (script + COPY command)
- Stage 3 — Git repo setup and example commits
- Stage 4 — Data cleaning & staging exports
- Stage 5 — Star schema creation
- Stage 6 — SQL analytics (funnel, cohort, segmentation, sessions)
- Stage 7 — Python analysis + plots
- Stage 8 — Dashboard guide & sample images
- Stage 9 — Business insights + experiments
- Stage 10 — Final README, resume bullets, merge into `main`
