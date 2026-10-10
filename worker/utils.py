from datetime import datetime, timedelta
import json
import logging

from dateutil.parser import isoparse
from sqlalchemy import desc, func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.models.area import Area
from app.core.config import settings
from app.models.salary import Salary
from app.models.employer import Employer
from app.models.vacancy import Vacancy
from app.models.hhParserState import HHParserState
from app.core.hhClient import hhClient

logger = logging.getLogger(__name__)

async def get_state(session):
    result = await session.execute(
        select(HHParserState).where(HHParserState.done == False).limit(1)
    )
    state = result.scalar()

    if state is None:
        await update_state(session)
        result = await session.execute(
            select(HHParserState).where(HHParserState.done == False).limit(1)
        )
        state = result.scalar()
    return state

async def close_interval_states(session, state):
    stmt = (
            update(HHParserState)
            .where(
                HHParserState.date_from == state.date_from,
                HHParserState.date_to == state.date_to,
                HHParserState.page >= state.page,
                HHParserState.done == False,
            )
            .values(done=True)
    )
    await session.execute(stmt)
    await session.commit()

async def update_state(session):
    stmt = await session.execute(
        select(HHParserState.date_to).order_by(desc(HHParserState.date_to))
    )

    last_state = stmt.scalar()
    rows = []
    today = datetime.today()
    if last_state is None:
        last_state = today - timedelta(days=30)
    else:
        current_start_date = max(last_state, today - timedelta(days=30))

    while current_start_date < today:
        current_end_date = current_start_date + timedelta(minutes=settings.time_interval_minutes)
        rows.append(HHParserState(
            date_from=current_start_date,
            date_to=current_end_date,
            per_page=settings.per_page,
            page=0,
            done=False,
        ))
        current_start_date = current_end_date

    if rows:
        session.add_all(rows)   
        await session.commit()

async def refresh_areas(session):
    client = hhClient()
    areas_raw = client.fetch_area()
    areas = flatten_areas(areas_raw)

    CHUNK = 8000
    for i in range(0, len(areas), CHUNK):
        stmt = (
            insert(Area)
            .values(areas[i:i + CHUNK])
            .on_conflict_do_nothing(index_elements=[Area.id])
        )
        await session.execute(stmt)
        
    await session.commit()

async def parse_hh_data(session):
    client = hhClient()
    state = await get_state(session)
    logger.info("parsing interval %s %s", state.date_from, state.date_to)
    while True:
        data = client.fetch_vacancies({
            "page": state.page, 
            "per_page": state.per_page, 
            "date_from": state.date_from.isoformat(),
            "date_to": state.date_to.isoformat(),
            })
        items = data.get("items", [])
        pages = data.get("pages")
        if not items:
            state.done = True
            logger.info("state date_from=%s date_to=%s have 0 entries on page %s, state closed",
                        state.date_from, state.date_to, state.page)
            await session.commit()
            return

        vacancy_values = [map_vacancy(i) for i in items]
        employer_values = [map_employer(i) for i in items]
        salary_values = [map_salary(i) for i in items]

        stmt = insert(Vacancy).values(vacancy_values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[Vacancy.id])
        await session.execute(stmt)

        stmt = insert(Salary).values(salary_values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Salary.vacancy_id],
            set_= {
                "s_from" : stmt.excluded.s_from,
                "s_to" : stmt.excluded.s_to,
                "currency" : stmt.excluded.currency,
                "gross" : stmt.excluded.gross,
            },
        )
        await session.execute(stmt)

        stmt = insert(Employer).values(employer_values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[Employer.name])
        await session.execute(stmt)

        logger.info("page %s done: vacancies=%s salaries=%s employers=%s",
                            state.page, len(vacancy_values), len(salary_values), len(employer_values))
        state.page += 1
        if state.page >= pages:
            state.done = True
            logger.info("state was closed date_from=%s date_to=%s after %s pages", 
                        state.date_from, state.date_to, state.page)
            await session.commit()
            return
        await session.commit()

def flatten_areas(areas_raw) -> list[dict]:
    result = []

    def walk(items):
        for i in items:
            result.append({
                "id": int(i["id"]),
                "parent_id": int(i["parent_id"]) if i.get("parent_id") is not None else None,
                "name": i["name"],
            })
            if i.get("areas"):
                walk(i["areas"])

    walk(areas_raw)
    return result

def map_salary(item: dict) -> dict:
    _id = int(item["id"])
    sal = item.get("salary")
    if not sal:
        return {"vacancy_id": _id, "s_from": None, "s_to": None, "currency": None, "gross": None}

    _from = int(sal["from"]) if sal.get("from") else None
    _to = int(sal["to"]) if sal.get("to") else None

    return {
        "vacancy_id": _id,
        "s_from": _from,
        "s_to": _to,
        "currency": sal["currency"],
        "gross": sal["gross"],
    }


def map_employer(item: dict) -> dict:
    emp = item["employer"]
    return {
        "id": int(item["id"]),
        "name": emp["name"],
        "accredited_it_employer": emp.get("accredited_it_employer", False),
        "trusted": emp["trusted"],
    }


def map_vacancy(item: dict) -> dict:
    _id = int(item["id"])
    logger.debug("raw item: %s", json.dumps(item, ensure_ascii=False))
    return {
        "id": _id,
        "name": item["name"],
        "area_id": int(item["area"]["id"]),
        "publishied_at": item["published_at"],
        "requirement": item["snippet"]["requirement"],
        "responsobility": item["snippet"]["responsibility"],
        "schedule": item.get("schedule", {}).get("id", "unknown"),
        "prof_roles": item["professional_roles"][0]["name"],
        "exp": item["experience"]["id"],
        "empoyment": extract_id(item, "employment_form"),
        "employers_name": item["employer"]["name"],
    }

def extract_id(item: dict, key: str) -> str | None:
    """Достаёт item[key]["id"] безопасно; None, если поля нет."""
    block = item.get(key)
    if isinstance(block, dict):
        return block.get("id")
    return None