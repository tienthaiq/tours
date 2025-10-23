select
    customer.custkey as id,
    customer.name,
    customer.address,
    customer.phone,
    customer.acctbal,
    customer.mktsegment,
    customer.comment,

    nation.name as nation_name,
    region.na as region_name

from {{ ref("stg_tpch_sf1__customer") }} as customer
left join {{ ref("stg_tpch_sf1__nation") }} as nation
    on customer.nationkey = nation.nationkey
left join {{ ref("stg_tpch_sf1__region") }} as region
    on nation.regionkey = region.regionkey
