-- name: get-by-username^
SELECT id AS user_id,
       username,
       salt,
       hashed_password,
       created_at,
       updated_at
FROM users
WHERE username = :username
LIMIT 1;

-- name: by-id^
SELECT id AS user_id,
       username,
       salt,
       hashed_password,
       created_at,
       updated_at
FROM users
WHERE id = :user_id
LIMIT 1;

-- name: check^
SELECT id AS user_id,
    username,
    salt,
    hashed_password,
    created_at,
    updated_at
FROM users
WHERE id = :user_id
    AND username = :username
LIMIT 1;

-- name: create<!
INSERT INTO users (username, salt, hashed_password)
VALUES (:username, :salt, :hashed_password)
RETURNING id AS user_id, username;

-- name: delete!
DELETE FROM users
WHERE id = :user_id and username = :username;
