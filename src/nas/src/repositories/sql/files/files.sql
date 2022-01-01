-- name: get
SELECT path, filename, extension
FROM files
WHERE extension IN (
    SELECT DISTINCT(name)
    FROM extensions
)
LIMIT 10;

-- name: get-json$
SELECT
   json_agg(j) as d
FROM (
    SELECT
        json_build_object(
           'path', path,
           'filename', filename,
           'extension', extension
        ) as j
    FROM files
    GROUP BY id
) AS r;

-- name: reset!
TRUNCATE TABLE files;
