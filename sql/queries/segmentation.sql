-- ==========================================================
-- USER SEGMENTATION
-- Segment users based on activity and revenue
-- ==========================================================

WITH user_metrics AS (

SELECT
user_id,

COUNT(*) AS total_events,

COUNT(*) FILTER (WHERE revenue_flag = 1) AS purchases,

SUM(price) AS total_revenue

FROM fact_events

GROUP BY user_id

)

SELECT
user_id,
total_events,
purchases,
total_revenue,

CASE

WHEN total_revenue > 500 THEN 'high_value'

WHEN total_revenue BETWEEN 100 AND 500 THEN 'mid_value'

WHEN total_revenue > 0 THEN 'low_value'

ELSE 'non_paying'

END AS segment

FROM user_metrics;
\copy (
SELECT * FROM (
WITH user_metrics AS (
SELECT
user_id,
COUNT(*) total_events,
COUNT(*) FILTER (WHERE revenue_flag=1) purchases,
SUM(price) total_revenue
FROM fact_events
GROUP BY user_id
)
SELECT
user_id,
total_events,
purchases,
total_revenue,
CASE
WHEN total_revenue > 500 THEN 'high_value'
WHEN total_revenue BETWEEN 100 AND 500 THEN 'mid_value'
WHEN total_revenue > 0 THEN 'low_value'
ELSE 'non_paying'
END segment
FROM user_metrics
) t
) TO 'data/user_segments.csv' CSV HEADER;