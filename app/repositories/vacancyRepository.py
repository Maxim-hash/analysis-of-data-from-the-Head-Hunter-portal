from sqlalchemy import select

from app.models.vacancy import Vacancy


class VacancyRepository:
    def __init__(self, session):
        self.session = session

    async def get_vacancies(self):
        stmt = select(Vacancy)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_vacancy_by_id(self, vacancy_id):
        stmt = select(Vacancy).where(Vacancy.id == vacancy_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_vacancies_by_filters(self):
        pass