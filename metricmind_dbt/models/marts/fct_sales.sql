{{ config(materialized='table') }}

SELECT 
    s.order_id,
    s.customer_id,
    s.product_id,
    r.region_id,
    s.order_date AS date_id,
    s.quantity,
    s.discount_percent,
    s.discount_amount,
    s.shipping_cost,
    s.tax_amount,
    s.order_amount,
    s.profit_amount,
    s.profit_margin_percent,
    s.payment_method,
    s.shipping_method,
    s.traffic_source,
    s.device_type,
    s.delivery_days,
    s.order_status,
    CASE WHEN LOWER(s.returned) IN ('true', 'yes', '1') THEN TRUE ELSE FALSE END AS returned,
    s.review_rating,
    CASE WHEN LOWER(s.coupon_used) IN ('true', 'yes', '1') THEN TRUE ELSE FALSE END AS coupon_used,
    CASE WHEN LOWER(s.high_value_order) IN ('true', 'yes', '1') THEN TRUE ELSE FALSE END AS high_value_order
FROM {{ ref('stg_orders') }} s
LEFT JOIN {{ ref('dim_region') }} r 
    ON s.country = r.country 
   AND s.city = r.city 
   AND COALESCE(s.warehouse_region, '') = COALESCE(r.warehouse_region, '')