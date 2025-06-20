with source as (
  select * from {{ source('raw', 'users') }}
),
renamed as (
  select
    user_id,
    lower(gender) as gender,
    condition,
    date(signup_date) as signup_date,
    age
  from source
)
select * from renamed