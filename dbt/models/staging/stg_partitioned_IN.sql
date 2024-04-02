{{
    config(
        materialized='view'
    )
}}


with

    source as (select * from {{ source("staging", "partitioned_IN") }}),

    renamed as (

        select
            video_id,
            trending_date,
            title,
            channel_title,
            {{ dbt.safe_cast("category_id", api.Column.translate_type("integer")) }} as category_id,
            publish_time,
            tags,
            views,
            likes,
            dislikes,
            comment_count,
            thumbnail_link,
            comments_disabled,
            ratings_disabled,
            video_error_or_removed,
            description,
            country

        from source

    )

select *
from renamed

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
