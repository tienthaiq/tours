select
    cus.customer_id,
    cus.store_id,
    cus.first_name,
    cus.last_name,
    cus.email,
    cus.create_date,
    cus.last_update,
    cus.activebool as is_active,

    addr.address,
    addr.address2,
    addr.district,
    addr.postal_code,
    addr.phone,

    cit.city,
    ctr.country
from {{ ref("sakila__customer") }} as cus
left join {{ ref("sakila__address") }} as addr
    on cus.address_id = addr.address_id
left join {{ ref("sakila__city") }} as cit
    on addr.city_id = cit.city_id
left join {{ ref("sakila__country") }} as ctr
    on cit.country_id = ctr.country_id
