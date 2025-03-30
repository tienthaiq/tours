select
    pay.payment_id,
    pay.customer_id,
    pay.staff_id,
    pay.amount,
    pay.payment_date,

    rental.rental_store_id,
    1 as new_col
from {{ ref("sakila__payment") }} as pay
left join {{ ref("fct_rental") }} as rental on pay.rental_id = rental.rental_id
