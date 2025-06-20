with source as (
  select * from {{ source('raw', 'clinical_sessions') }}
),
renamed as (
  select
    session_id,
    user_id,
    coach_id,
    date(session_date) as session_date,
    session_type,
    outcome_score,
    nps_score
  from source
)
select * from renamed