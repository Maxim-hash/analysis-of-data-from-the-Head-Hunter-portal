from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import selectinload

from app.core.session import get_session
from app.models import Vacancy

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_vacancies(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):

    offset = (page - 1) * limit

    stmt = (
        select(Vacancy)
        .options(
            selectinload(Vacancy.salary),
        )
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    vacancies = result.scalars().all()

    count_stmt = select(func.count()).select_from(Vacancy)
    total = await session.scalar(count_stmt)
    pages = (total + limit - 1) // limit

    return templates.TemplateResponse(
        "vacancies.html",
        {
            "request": request,
            "vacancies": vacancies,
            "pagination": {
                "page": page,
                "pages": pages,
                "prev_page": page - 1 if page > 1 else None,
                "next_page": page + 1 if page < pages else None
            }
        }
    )

@router.get("/{vacancy_id}", response_class=HTMLResponse, name="read_vacancy")
async def read_vacancy(
    request: Request,
    vacancy_id: int,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
    result = await session.execute(stmt)
    vacancy = result.scalar_one_or_none()
    if not vacancy: 
        pass
    return templates.TemplateResponse(
        "vacancy_detail.html",
        {
            "request": request,
            "vacancy": vacancy
        }
    )