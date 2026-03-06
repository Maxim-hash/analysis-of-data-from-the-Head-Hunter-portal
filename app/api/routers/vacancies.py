from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.session import get_session
from app.models import Vacancy

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.get("/")
async def list_roles(session: AsyncSession = Depends(get_session)):
    stmt = select(Vacancy)
    result = await session.execute(stmt)
    roles = result.scalars().all()
    return [r for r in roles]
