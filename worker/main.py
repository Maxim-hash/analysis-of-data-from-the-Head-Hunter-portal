import asyncio
import logging

from app.core.session import AsyncSessionLocal
from app.core.config import settings
from worker.utils import refresh_areas, parse_hh_data

logger = logging.getLogger(__name__)


async def run_worker():
    logging.basicConfig(
        level=logging.DEBUG if getattr(settings, "debug", False) else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger.info("worker started: interval=%ss per_page=%s",
                settings.parser_interval_seconds, settings.per_page)
    async with AsyncSessionLocal() as session:
        await refresh_areas(session)

    while True:
        async with AsyncSessionLocal() as session:
            await parse_hh_data(session)
        await asyncio.sleep(settings.parser_interval_seconds)


if __name__ == "__main__":
     asyncio.run(run_worker())