# Product Analytics Dashboard (Power BI)

This dashboard visualizes key insights from the Product Analytics project.

Data sources come from SQL outputs and Python analysis.

---

# Data Files Used

Import the following CSV files into Power BI:


data/funnel_results.csv
data/cohort_retention.csv
data/user_segments.csv
data/session_metrics.csv


In Power BI Desktop:


Home → Get Data → Text/CSV


Load all four datasets.

---

# Dashboard Layout

Recommended layout:

| KPI Cards |
| Sessions | Avg Events | Avg Time |

| Funnel Chart | Segment Distribution |

| Retention Curve |

| Cohort Retention Heatmap |


---

# KPI Cards

Fields from:

`session_metrics.csv`

Create **Card visuals**:

| Metric | Field |
|------|------|
Total Sessions | total_sessions
Avg Events per Session | avg_events_per_session
Avg Session Duration | avg_session_minutes

---

# Funnel Chart

Source: `funnel_results.csv`

Visual type:


Funnel Chart


Values:


signup_users
page_view_users
cart_users
purchase_users


Stages:


Signup
Page View
Add To Cart
Purchase


This visual shows conversion drop-off.

---

# User Segmentation Chart

Source: `user_segments.csv`

Visual:


Clustered Column Chart


Fields:


Axis: segment
Values: Count of user_id


This shows distribution of:


high_value
mid_value
low_value
non_paying


---

# Retention Curve

Source:

`cohort_retention.csv`

Visual:


Line Chart


Fields:


X-axis: activity_month
Y-axis: retention_pct
Legend: cohort_month


This visual shows retention decay over time.

---

# Cohort Retention Heatmap

Visual:


Matrix


Rows:


cohort_month


Columns:


activity_month


Values:


retention_pct


Enable conditional formatting:


Background color scale


This creates a **cohort heatmap**.

---

# Optional DAX Measures

Create these measures in Power BI.

## Conversion Rate

```DAX
Conversion Rate =
DIVIDE(
SUM(funnel_results[purchase_users]),
SUM(funnel_results[signup_users])
)
Average Retention
Average Retention =
AVERAGE(cohort_retention[retention_pct])