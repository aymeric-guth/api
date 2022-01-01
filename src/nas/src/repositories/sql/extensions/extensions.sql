-- name: get
SELECT DISTINCT(name) FROM extensions;

-- name: reset!
TRUNCATE TABLE extensions;