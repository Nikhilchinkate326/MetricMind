{{ config(materialized='table') }}

SELECT 
    ROW_NUMBER() OVER (ORDER BY country, city, warehouse_region) AS region_id,
    country,
    city,
    warehouse_region
FROM (
    SELECT DISTINCT country, city, warehouse_region
    FROM {{ ref('stg_orders') }}
    WHERE country IS NOT NULL AND city IS NOT NULL
) sub