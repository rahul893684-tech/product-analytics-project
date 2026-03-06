Product Analytics & User Behavior Analysis

This project explores how user activity data can be transformed into useful product insights.
It simulates an event-tracking system for a digital product and builds an analytics pipeline on top of it.

The pipeline collects user events, stores them in PostgreSQL, runs analytical SQL queries, and produces visualizations that highlight user behavior patterns such as conversion funnels and retention.

The goal of the project was to practice building a small product analytics stack from scratch using open-source tools.

What This Project Does

The project takes raw user event data and converts it into insights that a product team could use to make decisions.

Main steps:

Generate synthetic user behavior data

Store the data in a PostgreSQL warehouse

Model the data using a simple star schema

Run analytical SQL queries (funnels, cohorts, segmentation)

Analyze results with Python

Visualize insights in a Power BI dashboard

The final result shows how user behavior can be analyzed to improve product performance and conversion.

Project Workflow

The pipeline follows this flow:

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
Dataset

The dataset is generated using a Python script so the project can be reproduced without external data.

Script:

data/generate_data.py

Dataset characteristics:

~220,000 events

~50,000 users

simulated activity across one year

Example columns:

Column	Description
user_id	unique identifier for each user
event_type	type of action (signup, page_view, add_to_cart, purchase)
timestamp	event timestamp
session_id	identifier for user sessions
device	device used by the user
country	user location
product_id	product viewed or purchased
price	product price
revenue_flag	indicates purchase events
How To Run The Project
1. Clone the repository
git clone https://github.com/rahul893684-tech/product-analytics-project.git
cd product-analytics-project
2. Generate the dataset
python data/generate_data.py

Output file:

data/events.csv
3. Create the PostgreSQL database
createdb product_analytics

Create the raw events table:

psql -d product_analytics -f sql/raw_events_table.sql

Load the dataset:

\copy raw_events
FROM 'data/events.csv'
CSV HEADER
4. Run the data cleaning pipeline
python python/cleaning.py

Generated files:

data/cleaned/stg_events.csv
data/cleaned/stg_users.csv
data/cleaned/stg_dates.csv
5. Create the analytics schema
psql -d product_analytics -f sql/schema.sql

This step creates the fact and dimension tables used for analytics queries.

6. Run SQL analytics queries
psql -d product_analytics -f sql/queries/funnel.sql
psql -d product_analytics -f sql/queries/cohort.sql
psql -d product_analytics -f sql/queries/segmentation.sql
psql -d product_analytics -f sql/queries/session_analysis.sql

These queries generate the following outputs:

data/funnel_results.csv
data/cohort_retention.csv
data/user_segments.csv
data/session_metrics.csv
7. Run Python analysis

Install dependencies:

pip install -r python/requirements.txt

Run the analysis script:

python python/analysis.py

Generated charts:

images/retention_curve.png
images/segment_distribution.png
8. Dashboard

A Power BI dashboard is included to visualize the results.

Visualizations include:

Funnel conversion rates

Cohort retention heatmap

Retention curves

User segmentation

Session engagement metrics

Setup instructions are available in:

dashboard/README.md
Key Insights From The Analysis

Some patterns observed in the data:

The largest drop in the funnel occurs between page view and add-to-cart

Retention declines significantly after the first month

A relatively small group of users contributes a large portion of revenue

Many active users never make a purchase

These patterns suggest opportunities for improving product conversion and user engagement.

Detailed recommendations are documented in:

docs/insights.md
Technologies Used
Tool	Purpose
PostgreSQL	analytical data warehouse
Python	data generation and analysis
Pandas	data manipulation
Matplotlib	visualization
SQL	analytical queries
Power BI	dashboard visualization
Git	version control
Repository Structure
product-analytics-project
│
├── data
├── docs
├── dashboard
├── images
├── python
├── sql
└── README.md
Project Summary

This project demonstrates how raw event data can be transformed into meaningful product analytics.

By combining SQL analytics, Python analysis, and BI dashboards, the project highlights how user behavior can be used to understand product performance and identify opportunities for growth.

Resume Bullet Points

• Built an end-to-end product analytics pipeline analyzing 220K+ simulated user events using PostgreSQL, Python, and Power BI.

• Designed a star schema warehouse model to support analytical queries on user behavior data.

• Implemented SQL analyses including conversion funnel analysis, cohort retention tracking, user segmentation, and session metrics.

• Used Python (Pandas, Matplotlib) to analyze query outputs and generate retention and segmentation visualizations.

• Created a Power BI dashboard to present insights on user engagement, conversion performance, and customer value segments.