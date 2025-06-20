
{% set condition_filter = '1=1' %}
{% if is_incremental() %}
  {% set condition_filter = 'session_date >= dateadd(day, -1, current_date)' %}
{% endif %}

select
  user_id,
  count(*) as total_sessions,
  avg(outcome_score) as avg_outcome_score,
  avg(nps_score) as avg_nps_score
from {{ ref('stg_sessions') }}
where {{ condition_filter }}
group by user_id;
