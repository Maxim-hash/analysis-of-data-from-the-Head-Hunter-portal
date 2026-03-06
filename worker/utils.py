from datetime import datetime, timedelta

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
        select(HHParserState).order_by(desc(HHParserState.date_to))
    )

    last_state = stmt.scalar()
    intervals = []
    today = datetime.today()
    if last_state is None:
        last_state = today - timedelta(days=30)
        current_start_date = last_state
    while current_start_date < today:
        current_end_date = current_start_date + timedelta(minutes=settings.time_interval_minutes)  # Интервал в один час
        intervals.append({
            'date_from': current_start_date.isoformat(),
            'date_to': current_end_date.isoformat()
        })
        current_start_date += timedelta(minutes=settings.time_interval_minutes+5)

    for interval in intervals:
        for page in range(0, 19):
            params = {
                'date_from': isoparse(interval["date_from"]),
                'date_to': isoparse(interval["date_to"]),
                'per_page': settings.per_page,
                'page': page,
                'done': False,
            }
            stmt = insert(HHParserState).values(params)
            await session.execute(stmt)
            await session.commit()

async def init_areas_if_needed(session):
    count = await session.scalar(select(func.count()).select_from(Area))

    if count and count > 0:
        return
    client = hhClient()
    areas_raw = client.fetch_area()
    areas = format(areas_raw)

    session.add_all(areas)
    await session.commit()

async def parse_hh_data(session):
    client = hhClient()
    while True:
        state = await get_state(session)
        print(state.id)
        data = client.fetch_vacancies({
            "page": state.page, 
            "per_page": state.per_page, 
            "date_from": state.date_from.isoformat(),
            "date_to": state.date_to.isoformat(),
            "page": state.page,
            })
        items = data.get("items", [])
        pages = data.get("pages")
        if not items:
            await close_interval_states(session, state)
            return

        vacancy_values = [map_vacancy(i) for i in items]
        employer_values = [map_employer(i) for i in items]
        salary_values = [map_salary(i) for i in items]

        stmt = insert(Vacancy).values(vacancy_values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[Vacancy.id])
        await session.execute(stmt)

        stmt = insert(Salary).values(salary_values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[Salary.id])
        await session.execute(stmt)

        stmt = insert(Employer).values(employer_values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[Employer.name])
        await session.execute(stmt)

        state.done = True
        session.add(state)
        await session.commit()

def format(areas_raw):
    data = []
    for i in areas_raw:
        _id = int(i["id"])
        _parent_id = int(i["parent_id"]) if i["parent_id"] is not None else None
        _name = i["name"]
        parent = [Area(id = _id, parent_id = _parent_id, name = _name)]
        child = [j for j in dop_format(i["areas"])]
        parent.extend(child)
        data.extend(parent)

    return data

def dop_format(b):
    if b == []:
        return  
    buffer = []
    for i in b:
        _id = int(i["id"])
        _parent_id = int(i["parent_id"]) if i["parent_id"] is not None else None
        _name = i["name"]
        temp = Area(id = _id, parent_id = _parent_id, name = _name)
        buffer.append(temp)
        if i["areas"] == []:
            continue
        buffer.extend(dop_format(i["areas"]))
    return buffer

def map_salary(item: dict) -> dict:
    _id = int(item["id"])
    sal = item.get("salary")
    if not sal:
        return {"id": _id, "s_from": None, "s_to": None, "currency": None, "gross": None}

    _from = int(sal["from"]) if sal.get("from") else None
    _to = int(sal["to"]) if sal.get("to") else None

    return {
        "id": _id,
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
        "empoyment": item["id"],
        "employers_name": item["employer"]["name"],
    }
