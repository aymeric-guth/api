-- name: get
SELECT
    transducer_id,
    created_at,
    frequency,
    temperature
FROM model
ORDER BY 2, 1;