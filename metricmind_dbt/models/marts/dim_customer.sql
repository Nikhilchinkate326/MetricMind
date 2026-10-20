{{ config(materialized='table') }}

SELECT DISTINCT ON (customer_id)
    customer_id,
    customer_age,
    customer_gender,
    customer_segment,
    membership_status,
    customer_lifetime_value
FROM {{ ref('stg_orders') }}
WHERE customer_id IS NOT NULL