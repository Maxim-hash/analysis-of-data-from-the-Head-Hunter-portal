from sqlalchemy import func, select

from core.models.area import Area
from core.hhClient import hhClient


async def get_state(session):
    pass

async def init_areas_if_needed(session):
    count = await session.scalar(select(func.count()).select_from(Area))

    if count and count > 0:
        return
    client = hhClient()
    areas_raw = client.fetch_area()
    areas = format(areas_raw)

    session.add_all(areas)
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