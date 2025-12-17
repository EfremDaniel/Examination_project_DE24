with 
tr as (select * from {{ source('trafikanalys', 'trafik_analys') }})

select
    id,
    AR as 'year',
    Drivmedel as fuel,
    antal_i_trafik as car_in_traffic,
    l_n as county,
    kommun as municipality
from tr
where 
    AR between 2016 and 2024
    and Drivmedel in ['El', 'Elhybrid', 'Laddhybrid']
order by
    AR desc