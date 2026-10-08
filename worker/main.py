import asyncio

from app.core.session import AsyncSessionLocal
from app.core.config import settings
from worker.utils import refresh_areas, parse_hh_data


async def run_worker():
    async with AsyncSessionLocal() as session:
        await refresh_areas(session)

    while True:
        async with AsyncSessionLocal() as session:
            await parse_hh_data(session)
        await asyncio.sleep(settings.parser_interval_seconds)


if __name__ == "__main__":
     asyncio.run(run_worker())