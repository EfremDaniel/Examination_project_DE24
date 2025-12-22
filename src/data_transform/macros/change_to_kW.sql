{% macro kW(column) %}

    case trim(lower({{ column }}))
        when '250 kw dc' then 250
        when '350 kw dc' then 350
        when '225 kw dc' then 225
        when '62,5 kw dc' then 62.5
        when '500 kw dc' then 500
        when '400 kw dc' then 400
        when '75 kw dc' then 75
        when '150 kw dc' then 150
        when '200 kw dc' then 200
        when '300 kw dc' then 300
        when '135 kw - 480vdc max 270a' then 135
        when '100 kw - 500vdc max 200a' then 100
        when '180 kw dc' then 180
        when '175 kw dc' then 175
        when '22 kw - 400v 3-phase max 32a' then 22
        when '7,4 kw - 230v 1-phase max 32a' then 7.4
        when '3,6 kw - 230v 1-phase max 16a' then 3.6
        when '43 kw - 400v 3-phase max 63a' then 43
        when '50 kw - 500vdc max 100a' then 50
        when '20 kw - 500vdc max 50a'then 20

        else null
    end 
     
{% endmacro %}