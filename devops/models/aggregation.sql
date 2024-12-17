SELECT 
    post_type_id,
    COUNT(*) AS total_posts
FROM 
    {{ source('data_devops', 'posts') }}
GROUP BY 
    post_type_id
ORDER BY 
    total_posts DESC
