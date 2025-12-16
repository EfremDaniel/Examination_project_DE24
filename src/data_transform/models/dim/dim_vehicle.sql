with tr as (select * from {{ ref('src_trafikanalys') }})

select
    
    max(year),
    max(car_in_traffic),
    max(fuel)

from tr
