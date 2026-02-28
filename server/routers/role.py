from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.db import get_session
from models import Role

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/")
async def list_roles(session: AsyncSession = Depends(get_session)):
    stmt = select(Role)
    result = await session.execute(stmt)
    roles = result.scalars().all()
    return [{"id": r.id, "name": r.name} for r in roles]