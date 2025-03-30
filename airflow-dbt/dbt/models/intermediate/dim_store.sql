select
    store.store_id,
    store.manager_staff_id,
    store.last_update,

    addr.address,
    addr.address2,
    addr.district,
    addr.postal_code,
    addr.phone,

    cit.city,
    ctr.country
from {{ ref("sakila__store") }} as store
left join {{ ref("sakila__address") }} as addr
    on store.address_id = addr.address_id
left join {{ ref("sakila__city") }} as cit
    on addr.city_id = cit.city_id
left join {{ ref("sakila__country") }} as ctr
    on cit.country_id = ctr.country_id
