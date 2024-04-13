from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from model.src.BaseOrm import Base
from model.src.Orms import *
from model.src.Query_Builder import Query_Builder

class Database_handler:
    def __init__(self) -> None:
        self.async_engine = create_async_engine(url=settings.DATABASE_URL(), echo=True)
        self.async_session_factory = sessionmaker(self.async_engine, class_=AsyncSession)

    async def execute(self, string, commit=False):
        async with self.async_engine.connect() as conn:
            res = await conn.execute(text(string))
            if commit:
                await conn.commit()
        return res

    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    def select_from_table(self, table):
        pass

    async def insert_into_table(self, formatted_data):
        async with self.async_session_factory() as session:
            for model in formatted_data:
                for i in range(0, len(formatted_data[model]), 2048):
                        try:    
                            async with session.begin():
                                session.add_all(formatted_data[model][i:i+2048])
                                await session.commit()
                        except IntegrityError as e:
                            print(f"A database integrity error occurred: {e}")

        return True

    def update_table(data):
        pass

    async def drop_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
