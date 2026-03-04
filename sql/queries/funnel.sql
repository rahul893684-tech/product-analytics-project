-- ==========================================================
-- FUNNEL ANALYSIS
-- signup → page_view → add_to_cart → purchase
-- ==========================================================

WITH stage_users AS (

    SELECT
        user_id,

        MAX(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END) AS signup,

        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) AS page_view,

        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS add_to_cart,

        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchase

    FROM fact_events
    GROUP BY user_id
),

counts AS (

SELECT
    COUNT(*) FILTER (WHERE signup = 1) AS signup_users,
    COUNT(*) FILTER (WHERE page_view = 1) AS page_view_users,
    COUNT(*) FILTER (WHERE add_to_cart = 1) AS cart_users,
    COUNT(*) FILTER (WHERE purchase = 1) AS purchase_users

FROM stage_users

)

SELECT
    signup_users,
    page_view_users,
    cart_users,
    purchase_users,

    ROUND(page_view_users::numeric / signup_users * 100,2) AS signup_to_view_pct,

    ROUND(cart_users::numeric / page_view_users * 100,2) AS view_to_cart_pct,

    ROUND(purchase_users::numeric / cart_users * 100,2) AS cart_to_purchase_pct,

    ROUND(purchase_users::numeric / signup_users * 100,2) AS overall_conversion_pct

FROM counts;
\copy (
SELECT * FROM (
WITH stage_users AS (
    SELECT user_id,
    MAX(CASE WHEN event_type='signup' THEN 1 ELSE 0 END) signup,
    MAX(CASE WHEN event_type='page_view' THEN 1 ELSE 0 END) page_view,
    MAX(CASE WHEN event_type='add_to_cart' THEN 1 ELSE 0 END) add_to_cart,
    MAX(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END) purchase
    FROM fact_events
    GROUP BY user_id
),
counts AS (
SELECT
COUNT(*) FILTER (WHERE signup=1) signup_users,
COUNT(*) FILTER (WHERE page_view=1) page_view_users,
COUNT(*) FILTER (WHERE add_to_cart=1) cart_users,
COUNT(*) FILTER (WHERE purchase=1) purchase_users
FROM stage_users
)
SELECT
signup_users,
page_view_users,
cart_users,
purchase_users,
ROUND(page_view_users::numeric/signup_users*100,2) signup_to_view_pct,
ROUND(cart_users::numeric/page_view_users*100,2) view_to_cart_pct,
ROUND(purchase_users::numeric/cart_users*100,2) cart_to_purchase_pct,
ROUND(purchase_users::numeric/signup_users*100,2) overall_conversion_pct
FROM counts
) t
) TO 'data/funnel_results.csv' CSV HEADER;