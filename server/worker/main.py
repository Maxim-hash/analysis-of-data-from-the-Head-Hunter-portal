import asyncio

from core.db import AsyncSessionLocal
from worker.utils import init_areas_if_needed


async def run_worker():
    async with AsyncSessionLocal() as session:
        await init_areas_if_needed(session)


if __name__ == "__main__":
     asyncio.run(run_worker())