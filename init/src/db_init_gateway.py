import os
import asyncio

import asyncpg


HOST = os.getenv('DB_HOST_GATEWAY')
PORT = os.getenv('DB_PORT_GATEWAY')
USERNAME = os.getenv('DB_USER_GATEWAY')
PASSWORD = os.getenv('DB_PASSWORD_GATEWAY')
DATABASE_NAME = os.getenv('DB_NAME_GATEWAY')


async def main():
    connection = await asyncpg.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    ### Création Tables ###
    await connection.execute('''
        DROP TABLE IF EXISTS authorizations CASCADE;
    ''')
    await connection.execute('''
        DROP TABLE IF EXISTS services;
    ''')
    await connection.execute('''
        DROP TABLE IF EXISTS users;
    ''')
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT NULL,
            username VARCHAR,
            hashed_password VARCHAR,
            salt VARCHAR
        );
    ''')
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            route VARCHAR NOT NULL
        );
    ''')
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS authorizations (
            user_id BIGINT NOT NULL,
            service_id BIGINT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT Now(),
            updated_at TIMESTAMPTZ DEFAULT NULL,
            PRIMARY KEY (user_id, service_id),
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON UPDATE CASCADE,
            FOREIGN KEY (service_id)
                REFERENCES services(id)
                ON UPDATE CASCADE
        );
    ''')


    ### Insertion Données Test ###
    data = (
        # 1, 
        'yul',
        '$2b$12$x65w2Xqd5N/IRfC1y5EIEeT5zO9Wn.VpBUR6om43DGuV6B0PqS4A2',
        '$2b$12$WacuQWfasp8Uu.JLmMEwzO'
    )
    await connection.execute('''
        INSERT INTO users (username, hashed_password, salt)
        VALUES ($1, $2, $3)
        ON CONFLICT DO NOTHING;
    ''', *data)

    data = ('NAS', '/nas')
    await connection.execute('''
        INSERT INTO services (name, route)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING;
    ''', *data)

    data = (1, 1)
    await connection.execute('''
        INSERT INTO authorizations (user_id, service_id)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING;
    ''', *data)

    print("Database INIT GATEWAY: Done")
    await connection.close()

asyncio.run(main())
