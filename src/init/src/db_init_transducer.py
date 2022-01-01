import os
import asyncio

import asyncpg


HOST = os.getenv('DB_HOST_TR')
PORT = os.getenv('DB_PORT_TR')
USERNAME = os.getenv('DB_USER_TR')
PASSWORD = os.getenv('DB_PASSWORD_TR')
DATABASE_NAME = os.getenv('DB_NAME_TR')
print(
    HOST,
    PORT,
    USERNAME,
    PASSWORD,
    DATABASE_NAME,
)

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
        create table if not exists transducer (
            id bigserial primary key,
            id_bis bigint,
            ref varchar
        );
    ''')
    try:
        await connection.execute('''
            insert into transducer (id, id_bis, ref)
            values (1, 1, ''), (2, 2, ''), (3, 3, ''), (4, 4, '');
        ''')
    except Exception as err:
        pass
    await connection.execute('''
        create table if not exists model (
            id bigserial not null primary key,
            transducer_id bigint
            references transducer(id)
                on update cascade,
            created_at timestamp with time zone,
            status integer,
            cause integer,
            mode integer,
            frequency integer,
            pe integer,
            ps integer,
            minutes integer,
            vah integer,
            temperature integer
        );
    ''')
    print("Database INIT TRANSDUCER: Done")
    await connection.close()

asyncio.run(main())
