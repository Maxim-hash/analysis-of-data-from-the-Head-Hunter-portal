from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from model.src.BaseOrm import Base
from model.src.Orms import *
from model.src.Query_Builder import *

class Database_handler:
    def __init__(self) -> None:
        self.async_engine = create_async_engine(url=settings.ASYNC_DATABASE_URL(), echo=True)
        self.async_session_factory = sessionmaker(self.async_engine, class_=AsyncSession)
        self.sync_engine = create_engine(url=settings.SYNC_DATABASE_URL(), echo=True)
        self.sync_session_factory = sessionmaker(self.sync_engine)

    async def execute(self, string, commit=False):
        async with self.async_engine.connect() as conn:
            res = await conn.execute(text(string))
            if commit:
                await conn.commit()
        return res

    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get(self, orm, primary_key):
        async with self.async_session_factory() as session:
            data = await session.get(orm, primary_key)
        return data
    
    async def add(self, data):
        async with self.async_session_factory() as session:
            async with session.begin():
                session.add(data)
        return True
            
    def select(self, data, mode):
        with self.sync_session_factory() as session:
            with session.begin(): 
                if mode == "Vacancy":
                    query_builder = QueryBuilder(session, VacancyOrm)
                    query_builder.add_filter(ProfessionFilter(data[0]))
                    query_builder.add_filter(RegionFilter(session, data[1]))
                    query_builder.add_filter(ExperienceFilter(data[2]))
                elif mode == "Salary":
                    query_builder = QueryBuilder(session, SalaryOrm)
                    query_builder.add_filter(IdFilter(data.id))
                
                query = query_builder.build()
                
                result = query.all()
                session.expunge_all()

            return result

    async def insert_into_table(self, formatted_data):
        async with self.async_session_factory() as session:
            try:    
                async with session.begin():
                    session.add_all(formatted_data)

            except IntegrityError as e:
                print(f"A database integrity error occurred: {e}")

        return True

    def update_table(data):
        pass

    async def drop_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
