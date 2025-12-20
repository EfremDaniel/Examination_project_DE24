with
csmd_dump as (select * from {{ source('chargerstation', 'csmd_dump') }}),
csmd_update_dedup as ({{dbt_utils.deduplicate(
    relation= source('chargerstation', 'csmd_update'),
    partition_by= 'id',
    order_by='updated desc' 
)}}
),
dump_filter as (
    select
        cd.id,
        cd.name,
        cd.street,
        cd.zipcode,
        cd.city,
        cd.municipality_id,
        cd.municipality,
        cd.county_id,
        cd.county,
        cd.owned_by,
        cd.operator,
        cd.number_charging_points,
        cd.available_charging_points,
        cd.house_number,
        cd.updated,
        cd.created
    from csmd_dump cd
    where not exists (
    select 1
    from csmd_update_dedup cud
    where cd.id = cud.id
  )
),
updates as (
    select
        cud.id,
        cud.name,
        cud.street,
        cud.zipcode,
        cud.city,
        cud.municipality_id,
        cud.municipality,
        cud.county_id,
        cud.county,
        cud.owned_by,
        cud.operator,
        cud.number_charging_points,
        cud.available_charging_points,
        cud.house_number,
        cud.updated,
        cud.created
    from csmd_update_dedup cud 
),
final_table as (
    select * from dump_filter
    union all
    select * from updates
)

select * from final_table


