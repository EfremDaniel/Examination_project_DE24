with 
st_dump as (select * from {{ source('chargerstation', 'st_dump') }}),
st_update_debup as ({{dbt_utils.deduplicate(
relation= source('chargerstation', 'st_update'),
partition_by= 'station_id',
order_by= 'updated_date')
}}
),

st_dump_filter as (
    select
    station_id,
    attrname,
    attrtypeid,
    attrvalid
    from st_dump as ad
    where not exists(
        select 1
        from st_update_debup sud 
        where ad.station_id = sud.station_id
    )
),

updates as (
    select
    station_id,
    attrname,
    attrtypeid,
    attrvalid
from st_update_debup sud
),

final_table as (
    select * from st_dump_filter
    union 
    select * from updates
)
select * from final_table;