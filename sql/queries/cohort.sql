-- ==========================================================
-- COHORT RETENTION ANALYSIS
-- signup cohort month vs retention month
-- ==========================================================

WITH first_signup AS (

SELECT
user_id,
MIN(event_timestamp) AS signup_time
FROM fact_events
WHERE event_type = 'signup'
GROUP BY user_id

),

user_activity AS (

SELECT
f.user_id,
DATE_TRUNC('month', fs.signup_time) AS cohort_month,
DATE_TRUNC('month', f.event_timestamp) AS activity_month
FROM fact_events f
JOIN first_signup fs
ON f.user_id = fs.user_id

),

cohort_counts AS (

SELECT
cohort_month,
activity_month,
COUNT(DISTINCT user_id) AS active_users
FROM user_activity
GROUP BY cohort_month, activity_month

),

cohort_size AS (

SELECT
cohort_month,
COUNT(DISTINCT user_id) AS cohort_users
FROM user_activity
GROUP BY cohort_month

)

SELECT
c.cohort_month,
c.activity_month,
c.active_users,
s.cohort_users,
ROUND(c.active_users::numeric / s.cohort_users * 100,2) AS retention_pct

FROM cohort_counts c
JOIN cohort_size s
ON c.cohort_month = s.cohort_month

ORDER BY cohort_month, activity_month;
\copy (
SELECT * FROM (
-- cohort query
WITH first_signup AS (
SELECT user_id, MIN(event_timestamp) signup_time
FROM fact_events
WHERE event_type='signup'
GROUP BY user_id
),
user_activity AS (
SELECT
f.user_id,
DATE_TRUNC('month',fs.signup_time) cohort_month,
DATE_TRUNC('month',f.event_timestamp) activity_month
FROM fact_events f
JOIN first_signup fs ON f.user_id=fs.user_id
),
cohort_counts AS (
SELECT cohort_month,activity_month,COUNT(DISTINCT user_id) active_users
FROM user_activity
GROUP BY cohort_month,activity_month
),
cohort_size AS (
SELECT cohort_month,COUNT(DISTINCT user_id) cohort_users
FROM user_activity
GROUP BY cohort_month
)
SELECT
c.cohort_month,
c.activity_month,
c.active_users,
s.cohort_users,
ROUND(c.active_users::numeric/s.cohort_users*100,2) retention_pct
FROM cohort_counts c
JOIN cohort_size s
ON c.cohort_month=s.cohort_month
ORDER BY cohort_month,activity_month
) t
) TO 'data/cohort_retention.csv' CSV HEADER;