with
csmd_dump as (select * from {{ source('chargerstation', 'csmd_dump') }}),
csmd_update as (select * from {{ source('chargerstation', 'csmd_update') }}),

dump_filter as (
    select
        cd.id,
        cd.number_charging_points,
        cd.available_charging_points,
        cd.house_number
    from csmd_dump cd
    where not exists (
        select 1
        from csmd_update cu
        where cd.id = cu.id
    )
),
updates as (
    select
        cu.id,
        cu.number_charging_points,
        cu.available_charging_points,
        cu.house_number
    from csmd_update cu
),
final_table as (
    select * from dump_filter
    union all
    select * from updates
)

select * from final_table;



