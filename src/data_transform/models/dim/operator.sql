with owned_operator as (select * from {{ ref('src_csmd') }})


select 
    {{dbt_utils.generate_surrogate_key(['operator'])}} as operator_id,
    operator
from 
    owned_operator
group by operator

{# select
    operator_id,
    count(*) as n
from t 
group by operator_id
having count(*) > 1 #}








