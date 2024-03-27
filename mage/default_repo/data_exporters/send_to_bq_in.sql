CREATE OR REPLACE TABLE country_data.partitioned_in (
  video_id STRING,
  trending_date TIMESTAMP,
  title STRING,
  channel_title STRING,
  category_id STRING,
  publish_time TIMESTAMP,
  tags STRING,
  views STRING,
  likes STRING,
  dislikes STRING,
  comment_count INT64,
  thumbnail_link STRING,
  comments_disabled BOOL,
  ratings_disabled BOOL,
  video_error_or_removed BOOL,
  description STRING,
  country STRING
)
    PARTITION BY DATE(trending_date) AS 
SELECT
    video_id,
    TIMESTAMP_MICROS(CAST(trending_date/1000 AS INT)),
    title,
    channel_title,
    category_id,
    TIMESTAMP_MICROS(CAST(publish_time/1000 AS INT)),
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
FROM {{ df_1 }}