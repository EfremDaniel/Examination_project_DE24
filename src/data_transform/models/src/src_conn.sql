with conn_dump as (select * from {{ source('chargerstation', 'conn_dump') }}),
conn_update_dedup as ({{dbt_utils.deduplicate(
    relation= source('chargerstation', 'conn_update'),
    partition_by= 'station_id',
    order_by= "updated_date"
)}}),

conn_dump_filter as (
    select
        station_id,
        connector_nr,
        attrtypeid,
        attrname,
        attrvalid,
        trans
    from conn_dump cd 
    where not exists (
        select 
        1
        from conn_update_dedup cud 
        where cd.station_id = cud.station_id
    )
),

updates as (
    select
        station_id,
        connector_nr,
        attrtypeid,
        attrname,
        attrvalid,
        trans
    from conn_update_dedup
),

final_table as (
    select * from conn_dump_filter
    union
    select * from updates
)

select * from final_table