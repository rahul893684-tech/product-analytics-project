import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid
import os

# ----------------------------
# CONFIG
# ----------------------------
NUM_USERS = 50000
NUM_EVENTS = 220000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

devices = ["mobile", "desktop", "tablet"]
countries = ["US", "UK", "DE", "IN", "CA", "FR", "AU"]
event_types = ["signup", "page_view", "add_to_cart", "purchase"]

product_ids = [f"P{i}" for i in range(1, 51)]

price_map = {p: round(random.uniform(10, 200), 2) for p in product_ids}

# ----------------------------
# Helpers
# ----------------------------

def random_timestamp():
    delta = END_DATE - START_DATE
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return START_DATE + timedelta(seconds=random_seconds)


def generate_session_id():
    return str(uuid.uuid4())[:12]


# ----------------------------
# Generate Users
# ----------------------------

users = [f"user_{i}" for i in range(NUM_USERS)]

# Track which users signed up
signup_users = set(random.sample(users, int(NUM_USERS * 0.8)))

rows = []

for i in range(NUM_EVENTS):

    user = random.choice(users)

    # Event probability distribution
    event = np.random.choice(
        event_types,
        p=[0.1, 0.65, 0.15, 0.10]
    )

    ts = random_timestamp()

    session = generate_session_id()

    device = random.choice(devices)

    country = random.choice(countries)

    product = random.choice(product_ids)

    price = price_map[product]

    revenue_flag = 1 if event == "purchase" else 0

    if revenue_flag == 0:
        price = 0

    rows.append([
        user,
        event,
        ts.isoformat(),
        session,
        device,
        country,
        product,
        price,
        revenue_flag
    ])


columns = [
    "user_id",
    "event_type",
    "timestamp",
    "session_id",
    "device",
    "country",
    "product_id",
    "price",
    "revenue_flag"
]

df = pd.DataFrame(rows, columns=columns)

os.makedirs("data", exist_ok=True)

df.to_csv("data/events.csv", index=False)

print("Dataset generated:")
print(df.head())
print("\nRows:", len(df))
print("\nSaved to data/events.csv")