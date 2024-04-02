{{ config(materialized="table") }}

with full_table as (
        select id, title AS category, "IN" as country
        from {{ ref("IN_category_id") }}

        union all

        select id, title AS category, "JP" as country
        from {{ ref("JP_category_id") }}

        union all

        select id, title AS category, "US" as country
        from {{ ref("US_category_id") }}
    )

select *
from full_table
