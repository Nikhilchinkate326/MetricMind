{{ config(materialized='table') }}

SELECT DISTINCT ON (product_id)
    product_id,
    product_category,
    product_subcategory,
    brand,
    unit_price
FROM {{ ref('stg_orders') }}
WHERE product_id IS NOT NULL