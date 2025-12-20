with conn as (select * from {{ ref('src_conn') }})

select 
    station_id,
    {{ dbt_utils.generate_surrogate_key(['conn.attrname', 'trans'])}} as conn_id,
    cast(conn.connector_nr as int) as connector_nr
from 
    conn

