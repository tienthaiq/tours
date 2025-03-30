select
    rent.rental_id,
    rent.customer_id,
    rent.staff_id,
    
    rent.rental_date,
    rent.return_date,
    rent.last_update,

    ivent.store_id as rental_store_id
from {{ ref("sakila__rental") }} as rent
left join {{ ref("sakila__inventory") }} as ivent
    on rent.inventory_id = ivent.inventory_id
