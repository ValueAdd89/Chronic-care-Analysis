select
  user_id,
  alert_type,
  count(*) as total_alerts,
  sum(case when resolved then 1 else 0 end) as resolved_alerts,
  avg(case when resolved then 1.0 else 0.0 end) as resolution_rate
from {{ ref('stg_alerts') }}
group by user_id, alert_type