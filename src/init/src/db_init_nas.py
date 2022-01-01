import os
import asyncio

import asyncpg


HOST = os.getenv('DB_HOST_NAS')
PORT = os.getenv('DB_PORT_NAS')
USERNAME = os.getenv('DB_USER_NAS')
PASSWORD = os.getenv('DB_PASSWORD_NAS')
DATABASE_NAME = os.getenv('DB_NAME_NAS')


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
        CREATE TABLE IF NOT EXISTS files (
            id BIGSERIAL PRIMARY KEY,
            path VARCHAR,
            filename VARCHAR,
            extension VARCHAR
        );
    ''')
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS extensions (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR
        );
    ''')
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS playback (
            id BIGSERIAL PRIMARY KEY,
            path VARCHAR,
            filename VARCHAR,
            extension VARCHAR,
            tc FLOAT
        );
    ''')

    print("Database INIT NAS: Done")
    await connection.close()

asyncio.run(main())
