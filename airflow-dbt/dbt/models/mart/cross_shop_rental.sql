select
    sum(case when cust.store_id != rent.rental_store_id then 1 else 0 end) cross_shop_rental_count,
    sum(case when cust.city != store.city then 1 else 0 end) cross_city_rental_count
from {{ ref("fct_rental") }} as rent
left join {{ ref("dim_customer") }} as cust
    on rent.customer_id = cust.customer_id
left join {{ ref("dim_store") }} as store
    on rent.rental_store_id = store.store_id
