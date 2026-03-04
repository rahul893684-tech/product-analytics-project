-- ==========================================================
-- SESSION ANALYSIS
-- Session counts and length
-- ==========================================================

WITH session_events AS (

SELECT
session_id,
MIN(event_timestamp) AS session_start,
MAX(event_timestamp) AS session_end,
COUNT(*) AS events_in_session

FROM fact_events

GROUP BY session_id

),

session_metrics AS (

SELECT
session_id,
events_in_session,

EXTRACT(EPOCH FROM (session_end - session_start)) / 60 AS session_minutes

FROM session_events

)

SELECT
COUNT(*) AS total_sessions,
AVG(events_in_session) AS avg_events_per_session,
AVG(session_minutes) AS avg_session_minutes

FROM session_metrics;
\copy (
SELECT * FROM (
WITH session_events AS (
SELECT
session_id,
MIN(event_timestamp) session_start,
MAX(event_timestamp) session_end,
COUNT(*) events_in_session
FROM fact_events
GROUP BY session_id
),
session_metrics AS (
SELECT
session_id,
events_in_session,
EXTRACT(EPOCH FROM (session_end-session_start))/60 session_minutes
FROM session_events
)
SELECT
COUNT(*) total_sessions,
AVG(events_in_session) avg_events_per_session,
AVG(session_minutes) avg_session_minutes
FROM session_metrics
) t
) TO 'data/session_metrics.csv' CSV HEADER;