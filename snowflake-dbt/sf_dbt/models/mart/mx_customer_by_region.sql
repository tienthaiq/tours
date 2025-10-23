select
    nation_name,
    region_name,
    count(1)
from {{ ref("dim_customer") }}
group by nation_name, region_name
