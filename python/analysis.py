import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# Paths
# -------------------------

COHORT_FILE = "data/cohort_retention.csv"
SEGMENT_FILE = "data/user_segments.csv"
SESSION_FILE = "data/session_metrics.csv"

IMAGE_DIR = "images"
REPORT_PATH = "python/report.md"

os.makedirs(IMAGE_DIR, exist_ok=True)

# -------------------------
# Load datasets
# -------------------------

print("Loading SQL outputs...")

cohort = pd.read_csv(COHORT_FILE)
segments = pd.read_csv(SEGMENT_FILE)
session = pd.read_csv(SESSION_FILE)

print("Cohort rows:", len(cohort))
print("Segments rows:", len(segments))

# -------------------------
# RETENTION CURVE
# -------------------------

print("Generating retention curve...")

cohort["cohort_month"] = pd.to_datetime(cohort["cohort_month"])
cohort["activity_month"] = pd.to_datetime(cohort["activity_month"])

cohort["months_since_signup"] = (
    (cohort["activity_month"].dt.year - cohort["cohort_month"].dt.year) * 12 +
    (cohort["activity_month"].dt.month - cohort["cohort_month"].dt.month)
)

retention = cohort.groupby("months_since_signup")["retention_pct"].mean()

plt.figure()
retention.plot(marker="o")
plt.title("User Retention Curve")
plt.xlabel("Months Since Signup")
plt.ylabel("Retention %")
plt.grid(True)

retention_path = f"{IMAGE_DIR}/retention_curve.png"
plt.savefig(retention_path)

print("Saved:", retention_path)

# -------------------------
# SEGMENT DISTRIBUTION
# -------------------------

print("Generating segment distribution...")

segment_counts = segments["segment"].value_counts()

plt.figure()

segment_counts.plot(kind="bar")

plt.title("User Segment Distribution")
plt.xlabel("User Segment")
plt.ylabel("User Count")

plt.xticks(rotation=45)   # rotate labels
plt.tight_layout()        # fix spacing

segment_path = f"{IMAGE_DIR}/segment_distribution.png"
plt.savefig(segment_path)

print("Saved:", segment_path)

# -------------------------
# Session Metrics
# -------------------------

total_sessions = session["total_sessions"].iloc[0]
avg_events = session["avg_events_per_session"].iloc[0]
avg_minutes = session["avg_session_minutes"].iloc[0]

# -------------------------
# Generate Markdown Report
# -------------------------

report = f"""
# Product Analytics Report

## Key Metrics

**Total Sessions:** {total_sessions}

**Average Events per Session:** {round(avg_events,2)}

**Average Session Duration (minutes):** {round(avg_minutes,2)}

---

## User Segments

{segment_counts.to_string()}

---

## Charts

Retention Curve  
![Retention](../images/retention_curve.png)

Segment Distribution  
![Segments](../images/segment_distribution.png)
"""

with open(REPORT_PATH, "w") as f:
    f.write(report)

print("Report saved to:", REPORT_PATH)