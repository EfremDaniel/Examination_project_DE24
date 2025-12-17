{% macro fill_street_nr(column) %}

    case 
        when {{ column }} = '' then 'no number'

        else {{ column }}

    end
  
{% endmacro %}