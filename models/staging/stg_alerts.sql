with source as (
  select * from {{ source('raw', 'ai_alerts') }}
),
renamed as (
  select
    alert_id,
    user_id,
    date(alert_date) as alert_date,
    alert_type,
    resolved::boolean as resolved
  from source
)
select * from renamed