with 

source as (

    select * from {{ source('staging', 'partitioned_JP') }}

),

renamed as (

    select
        video_id,
        trending_date,
        title,
        channel_title,
        category_id,
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

select * from renamed
