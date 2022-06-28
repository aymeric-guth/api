-- name: by-id^
SELECT id AS service_id,
       name,
       route
FROM services
WHERE id = :service_id
LIMIT 1;