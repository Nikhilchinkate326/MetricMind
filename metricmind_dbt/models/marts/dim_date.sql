{{ config(materialized='table') }}

SELECT DISTINCT
    order_date AS date_id,
    year,
    'Q' || quarter::text AS quarter,
    month,
    day,
    day_of_week,
    season,
    CASE 
        WHEN LOWER(holiday_season) IN ('true', 'yes', '1') THEN TRUE 
        ELSE FALSE 
    END AS holiday_season
FROM {{ ref('stg_orders') }}
WHERE order_date IS NOT NULL