-- name: get
SELECT tc, path, filename, extension
FROM playback;

-- name: reset!
TRUNCATE TABLE playback;