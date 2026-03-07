import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# Paths
# -------------------------

COHORT_FILE = "data/cohort_retention.csv"
SEGMENT_FILE = "data/user_segments.csv"
SESSION_FILE = "data/session_metrics.csv"
FUNNEL_FILE = "data/funnel_results.csv"

IMAGE_DIR = "images"
REPORT_DIR = "python"
REPORT_PATH = f"{REPORT_DIR}/report.md"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# -------------------------
# Load datasets
# -------------------------

print("Loading SQL outputs...")

cohort = pd.read_csv(COHORT_FILE)
segments = pd.read_csv(SEGMENT_FILE)
session = pd.read_csv(SESSION_FILE)
funnel = pd.read_csv(FUNNEL_FILE)

# -------------------------
# Retention Curve
# -------------------------

cohort["cohort_month"] = pd.to_datetime(cohort["cohort_month"])
cohort["activity_month"] = pd.to_datetime(cohort["activity_month"])

cohort["months_since_signup"] = (
    (cohort["activity_month"].dt.year - cohort["cohort_month"].dt.year) * 12 +
    (cohort["activity_month"].dt.month - cohort["cohort_month"].dt.month)
)

retention = cohort.groupby("months_since_signup")["retention_pct"].mean()

plt.figure()
retention.plot(marker="o")
plt.title("Retention Curve")
plt.xlabel("Months Since Signup")
plt.ylabel("Retention %")
plt.grid(True)

plt.savefig(f"{IMAGE_DIR}/retention_curve.png")
plt.close()

# -------------------------
# Cohort Heatmap
# -------------------------

pivot = cohort.pivot_table(
    index="cohort_month",
    columns="months_since_signup",
    values="retention_pct"
)

plt.figure()
plt.imshow(pivot, aspect="auto")
plt.colorbar(label="Retention %")

plt.title("Cohort Retention Heatmap")
plt.xlabel("Months Since Signup")
plt.ylabel("Cohort Month")

plt.xticks(range(len(pivot.columns)), pivot.columns)
plt.yticks(range(len(pivot.index)), pivot.index.strftime("%Y-%m"))

plt.tight_layout()

plt.savefig(f"{IMAGE_DIR}/cohort_heatmap.png")
plt.close()

# -------------------------
# Segment Distribution
# -------------------------

segment_counts = segments["segment"].value_counts()

plt.figure()
segment_counts.plot(kind="bar")

plt.title("User Segment Distribution")
plt.xlabel("Segment")
plt.ylabel("Users")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(f"{IMAGE_DIR}/segment_distribution.png")
plt.close()

# -------------------------
# Funnel Chart
# -------------------------

stages = [
    funnel["signup_users"].iloc[0],
    funnel["page_view_users"].iloc[0],
    funnel["cart_users"].iloc[0],
    funnel["purchase_users"].iloc[0]
]

labels = ["Signup","Page View","Add to Cart","Purchase"]

plt.figure()

plt.bar(labels, stages)

plt.title("User Funnel")
plt.ylabel("Users")

plt.tight_layout()

plt.savefig(f"{IMAGE_DIR}/funnel_chart.png")
plt.close()

# -------------------------
# Session Metrics Chart
# -------------------------

session_values = [
    session["avg_events_per_session"].iloc[0],
    session["avg_session_minutes"].iloc[0]
]

session_labels = ["Avg Events","Avg Minutes"]

plt.figure()

plt.bar(session_labels, session_values)

plt.title("Session Metrics")

plt.tight_layout()

plt.savefig(f"{IMAGE_DIR}/session_metrics.png")
plt.close()

# -------------------------
# Report
# -------------------------

report = f"""
# Product Analytics Report

## Key Metrics

Total Sessions: {session["total_sessions"].iloc[0]}

Average Events per Session: {round(session["avg_events_per_session"].iloc[0],2)}

Average Session Duration (minutes): {round(session["avg_session_minutes"].iloc[0],2)}

---

## Charts

### Retention Curve
![Retention](../images/retention_curve.png)

### Cohort Heatmap
![Heatmap](../images/cohort_heatmap.png)

### Funnel
![Funnel](../images/funnel_chart.png)

### Segment Distribution
![Segments](../images/segment_distribution.png)

### Session Metrics
![Session](../images/session_metrics.png)
"""

with open(REPORT_PATH, "w") as f:
    f.write(report)

print("Report generated.")