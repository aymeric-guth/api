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
    where extension in (select name from extensions)
    GROUP BY id
    order by char_length(path)
    LIMIT 1000
) AS r;


-- name: get-one^
SELECT *
FROM files
WHERE filename = :filename AND extension = :extension AND path = :path
LIMIT 1;

-- name: get-dir^
SELECT *
FROM files
WHERE path = :path
LIMIT 1;

-- name: delete-one!
DELETE 
FROM files
WHERE filename = :filename AND extension = :extension AND path = :path;


-- name: delete-path!
DELETE 
FROM files
WHERE path = :path;
