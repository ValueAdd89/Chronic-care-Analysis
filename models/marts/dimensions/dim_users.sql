select
  user_id,
  gender,
  condition,
  age,
  signup_date,
  case
    when age < 18 then 'Under 18'
    when age between 18 and 34 then '18-34'
    when age between 35 and 49 then '35-49'
    when age >= 50 then '50+'
  end as age_group
from {{ ref('stg_users') }}