import pandas as pd
import os

# -----------------------------
# Paths
# -----------------------------
RAW_DATA_PATH = "data/events.csv"
CLEAN_DIR = "data/cleaned"

os.makedirs(CLEAN_DIR, exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------

print("Loading raw dataset...")

df = pd.read_csv(RAW_DATA_PATH)

print("Initial shape:", df.shape)
print(df.head())

# -----------------------------
# Basic Inspection
# -----------------------------

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# -----------------------------
# Remove Duplicates
# -----------------------------

df = df.drop_duplicates()

# -----------------------------
# Timestamp Standardization
# -----------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract useful time features
df["event_date"] = df["timestamp"].dt.date
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()

# -----------------------------
# Data Type Fixes
# -----------------------------

df["price"] = df["price"].fillna(0)
df["revenue_flag"] = df["revenue_flag"].fillna(0)

df["device"] = df["device"].astype(str)
df["country"] = df["country"].astype(str)

# -----------------------------
# Create Event Staging Table
# -----------------------------

stg_events = df[[
    "user_id",
    "event_type",
    "timestamp",
    "session_id",
    "device",
    "country",
    "product_id",
    "price",
    "revenue_flag"
]]

# -----------------------------
# Create Users Dimension
# -----------------------------

stg_users = df.groupby("user_id").agg(
    first_event=("timestamp", "min"),
    last_event=("timestamp", "max"),
    total_events=("event_type", "count"),
    country=("country", "first"),
    device=("device", "first")
).reset_index()

# -----------------------------
# Create Date Dimension
# -----------------------------

dates = pd.DataFrame({
    "date": pd.to_datetime(df["event_date"].unique())
})

dates["year"] = dates["date"].dt.year
dates["month"] = dates["date"].dt.month
dates["day"] = dates["date"].dt.day
dates["weekday"] = dates["date"].dt.day_name()
dates["week_of_year"] = dates["date"].dt.isocalendar().week

stg_dates = dates.sort_values("date")

# -----------------------------
# Save Cleaned Files
# -----------------------------

stg_events.to_csv(f"{CLEAN_DIR}/stg_events.csv", index=False)
stg_users.to_csv(f"{CLEAN_DIR}/stg_users.csv", index=False)
stg_dates.to_csv(f"{CLEAN_DIR}/stg_dates.csv", index=False)

print("\nSaved cleaned datasets:")
print("data/cleaned/stg_events.csv")
print("data/cleaned/stg_users.csv")
print("data/cleaned/stg_dates.csv")

print("\nEvent rows:", len(stg_events))
print("Users:", len(stg_users))
print("Dates:", len(stg_dates))