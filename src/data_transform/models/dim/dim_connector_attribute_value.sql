with conn as (select * from {{ ref('src_conn') }})

select
    {{ dbt_utils.generate_surrogate_key(['conn.attrname', 'trans'])}} as conn_id,
    conn.attrname as attribute_name,
    trans 
from 
    conn 
group by attribute_name, trans

{# select
    conn_id,
    count(*) as n
from t 
group by conn_id
having count(*) > 1 #}