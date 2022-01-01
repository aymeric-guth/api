-- name: check^
SELECT *
FROM users AS u
JOIN authorizations as a
    ON (u.id = a.user_id)
JOIN services AS s
    ON (a.service_id = s.id)
WHERE s.route = :service_route
    AND u.id = :user_id;

-- name: check-delegate^
SELECT *
FROM users AS u
JOIN authorizations as a
    ON (u.id = a.user_id)
JOIN services AS s
    ON (a.service_id = s.id)
WHERE s.id = :service_id
    AND u.id = :user_id;

-- name: create!
INSERT INTO authorizations (user_id, service_id)
VALUES (:user_id, :service_id);

-- name: delete!
DELETE FROM authorizations
WHERE user_id = :user_id
    AND service_id = :service_id;
