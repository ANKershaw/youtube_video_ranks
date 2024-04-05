{{
    config(
        materialized='table'
    )
}}

with IN_trending as (
    select *
    from {{ ref('stg_partitioned_IN') }}
), 
JP_trending as (
    select *
    from {{ ref('stg_partitioned_JP') }}
), 
US_trending as (
    select *
    from {{ ref('stg_partitioned_US') }}
), 
categories as (
    select * from {{ ref('dim_categories') }}
),
videos_unioned as (
    select * from IN_trending
    union all 
    select * from JP_trending
    union all
    select * from US_trending
)

select videos_unioned.video_id,
    videos_unioned.trending_date,
    videos_unioned.title,
    videos_unioned.channel_title,
    category_id,
    videos_unioned.publish_time,
    videos_unioned.tags,
    videos_unioned.views,
    videos_unioned.likes,
    videos_unioned.dislikes,
    videos_unioned.comment_count,
    videos_unioned.thumbnail_link,
    videos_unioned.comments_disabled,
    videos_unioned.ratings_disabled,
    videos_unioned.video_error_or_removed,
    videos_unioned.description,
    videos_unioned.country,
    categories.category AS category_name
from videos_unioned
left join categories ON
videos_unioned.category_id = categories.id
AND
videos_unioned.country = categories.country

