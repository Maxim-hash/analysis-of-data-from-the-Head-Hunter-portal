import asyncio

from app.core.session import AsyncSessionLocal
from app.core.config import settings
from worker.utils import init_areas_if_needed, parse_hh_data


async def run_worker():
    async with AsyncSessionLocal() as session:
        await init_areas_if_needed(session)

    while True:
        async with AsyncSessionLocal() as session:
            await parse_hh_data(session)
        await asyncio.sleep(settings.parser_interval_seconds)


if __name__ == "__main__":
     asyncio.run(run_worker())