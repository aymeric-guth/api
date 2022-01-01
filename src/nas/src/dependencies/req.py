import httpx


async def req():
    client = httpx.AsyncClient()
    try:
        yield client
    finally:
        await client.aclose()
