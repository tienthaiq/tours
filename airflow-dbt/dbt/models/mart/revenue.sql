select
    payment_date::date as metrics_date,
    store.city,
    store.district,
    sum(amount) as revenue,
    count(1) as rental_count,
    sum(amount) / count(1) as avg_revenue_per_rental
from {{ ref("fct_payment") }} as pay
left join {{ ref("dim_store") }} as store on pay.rental_store_id = store.store_id
group by 1, 2, 3
