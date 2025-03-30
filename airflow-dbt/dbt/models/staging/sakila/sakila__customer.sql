select *
from {{ source("sakila", "customer") }}
