-- =============================================
-- STAR SCHEMA FOR PRODUCT ANALYTICS
-- PostgreSQL dialect
-- =============================================

-- -------------------------------
-- DIMENSION: USERS
-- -------------------------------

CREATE TABLE dim_users (
    user_id TEXT PRIMARY KEY,
    first_event TIMESTAMP,
    last_event TIMESTAMP,
    total_events INTEGER,
    country TEXT,
    device TEXT
);

-- -------------------------------
-- DIMENSION: DATE
-- -------------------------------

CREATE TABLE dim_date (
    date DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    weekday TEXT,
    week_of_year INTEGER
);

-- -------------------------------
-- FACT TABLE: EVENTS
-- -------------------------------

CREATE TABLE fact_events (
    event_id BIGSERIAL PRIMARY KEY,
    user_id TEXT,
    event_type TEXT,
    event_timestamp TIMESTAMP,
    session_id TEXT,
    device TEXT,
    country TEXT,
    product_id TEXT,
    price NUMERIC,
    revenue_flag INTEGER,

    event_date DATE,

    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    FOREIGN KEY (event_date) REFERENCES dim_date(date)
);

-- -------------------------------
-- INDEXES FOR PERFORMANCE
-- -------------------------------

CREATE INDEX idx_fact_user
ON fact_events(user_id);

CREATE INDEX idx_fact_event_type
ON fact_events(event_type);

CREATE INDEX idx_fact_event_date
ON fact_events(event_date);