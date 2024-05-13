import asyncio
from model.model import *
from model.src.database_handler import Database_handler
from model.src.Orms import *
from model.src.API_Grabber import *
from model.src.data_formatter import Data_Formatter

class API_Model( model):
    def __init__(self) -> None:
        self.db_handler = Database_handler()

    modes = {
        "vacancy" : 0,
        "area" : 1
    }

    async def refresh_tables(self):
        await self.db_handler.drop_table(SkillOrm.__table__)
        await self.db_handler.drop_table(SalaryOrm.__table__)
        await self.db_handler.drop_table(VacancyOrm.__table__)
        await self.db_handler.drop_table(EmployerOrm.__table__)
        await self.db_handler.drop_table(AreaOrm.__table__)
        await self.db_handler.create_tables()

    async def get_API_data(self, mode):
        if mode in self.modes:
            api_grabber = API_Grabber()
            raw_data = await api_grabber.get_data(mode)
            formatter = Data_Formatter(raw_data)
            formatted_data = formatter.format(mode)
            return formatted_data
        else:
            raise ValueError("Unsupported mode type")
        
    async def get_skill(self, id):
        api_grabber = API_Grabber()
        skills = await api_grabber.get_skills_data(id)
        return skills

    async def load_skills(self, id, data):
        await self.db_handler.add(SkillOrm(vacancy_id= id, skill = data))

    async def load_data_into_tables(self, formatted_data):

        for model in formatted_data:
            for i in range(0, len(formatted_data[model]), 2048):
                await self.db_handler.insert_into_table(formatted_data[model][i:i+2048])
    
            