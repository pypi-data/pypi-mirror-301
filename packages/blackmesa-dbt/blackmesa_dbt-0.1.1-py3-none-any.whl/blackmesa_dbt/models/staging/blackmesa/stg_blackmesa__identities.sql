{{ config(
    materialized='table',
    schema='blackmesa'
) }}

select
  cast(null as integer) as identifier,
  cast(null as integer) as name,
  cast(null as integer) as description,
  cast(null as varchar) as key
where 1 = 0

