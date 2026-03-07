# Product Analytics & User Behavior Analysis

This project demonstrates how raw user activity data can be transformed into actionable product insights. It simulates an event-tracking system for a digital product and builds an analytics pipeline to analyze user behavior.

The pipeline collects user events, stores them in PostgreSQL, performs analytical SQL queries, and generates visualizations that highlight user behavior patterns such as conversion funnels and retention.

The goal of this project is to practice building a small *product analytics stack from scratch using open-source tools*.

---

# What This Project Does

The project converts raw user event data into insights that a product team could use for decision-making.

Main steps:

- Generate synthetic user behavior data
- Store the data in a PostgreSQL warehouse
- Model the data using a star schema
- Run analytical SQL queries (funnels, cohorts, segmentation)
- Analyze results using Python
- Visualize insights in a Power BI dashboard

The final output demonstrates how user behavior analysis can help improve product performance and conversion.

---

# Project Workflow

The analytics pipeline follows this flow:

Synthetic Event Generator  
↓  
Raw CSV Dataset  
↓  
PostgreSQL Database  
↓  
Data Modeling (Star Schema)  
↓  
SQL Analytics  
↓  
Python Analysis  
↓  
Power BI Dashboard  
↓  
Product Insights

---

# Dataset

The dataset is generated using a Python script so the project can be reproduced without external data.

Script:


data/generate_data.py


### Dataset Characteristics

- ~220,000 events
- ~50,000 users
- Simulated activity across one year

### Example Columns

| Column | Description |
|------|-------------|
| user_id | Unique identifier for each user |
| event_type | Type of action (signup, page_view, add_to_cart, purchase) |
| timestamp | Event timestamp |
| session_id | Identifier for user sessions |
| device | Device used by the user |
| country | User location |
| product_id | Product viewed or purchased |
| price | Product price |
| revenue_flag | Indicates purchase events |

---

# How To Run The Project

### 1. Clone the Repository


git clone https://github.com/rahul893684-tech/product-analytics-project.git
cd product-analytics-project


---

### 2. Generate the Dataset


python data/generate_data.py


Output file:


data/events.csv


---

### 3. Create the PostgreSQL Database


createdb product_analytics


Create the raw events table:


psql -d product_analytics -f sql/raw_events_table.sql


Load the dataset:


\copy raw_events FROM 'data/events.csv' CSV HEADER


---

### 4. Run the Data Cleaning Pipeline


python python/cleaning.py


Generated files:


data/cleaned/stg_events.csv
data/cleaned/stg_users.csv
data/cleaned/stg_dates.csv


---

### 5. Create the Analytics Schema


psql -d product_analytics -f sql/schema.sql


This step creates the fact and dimension tables used for analytics queries.

---

### 6. Run SQL Analytics Queries


psql -d product_analytics -f sql/queries/funnel.sql
psql -d product_analytics -f sql/queries/cohort.sql
psql -d product_analytics -f sql/queries/segmentation.sql
psql -d product_analytics -f sql/queries/session_analysis.sql


These queries generate:


data/funnel_results.csv
data/cohort_retention.csv
data/user_segments.csv
data/session_metrics.csv


---

### 7. Run Python Analysis

Install dependencies:


pip install -r python/requirements.txt


Run the analysis script:


python python/analysis.py


Generated charts:


images/retention_curve.png
images/segment_distribution.png


---

### 8. Dashboard

A Power BI dashboard is included to visualize the results.

Visualizations include:

- Funnel conversion rates
- Cohort retention heatmap
- Retention curves
- User segmentation
- Session engagement metrics

Setup instructions are available in:


dashboard/README.md


---

# Key Insights From the Analysis

Some patterns observed in the data:

- The largest drop-off in the funnel occurs between *Page View → Add To Cart*
- Retention declines significantly after the first month
- A small group of users contributes a large portion of revenue
- Many active users never make a purchase

These findings suggest opportunities to improve *product conversion and user engagement*.

Detailed recommendations are documented in:


docs/insights.md


---

# Technologies Used

| Tool | Purpose |
|-----|--------|
| PostgreSQL | Analytical data warehouse |
| SQL | Analytical queries |
| Python | Data generation and analysis |
| Pandas | Data manipulation |
| Matplotlib | Visualization |
| Power BI | Dashboard visualization |
| Git | Version control |

---

# Repository Structure


product-analytics-project
│
├── data
├── docs
├── dashboard
├── images
├── python
├── sql
└── README.md


---

# Project Summary

This project demonstrates how raw event data can be transformed into meaningful product analytics.

By combining *SQL analytics, Python analysis, and BI dashboards*, the project shows how user behavior data can be used to understand product performance and identify opportunities for growth.

# Upgrade
The purpose of the project was to demonstrate the data engineering and analytics pipeline rather than the dataset itself. If I were extending this project further, I would improve the event generator to simulate churn, realistic session behavior, and long-tail revenue distributions.