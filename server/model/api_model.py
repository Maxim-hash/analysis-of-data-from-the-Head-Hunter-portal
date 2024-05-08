from model.model import *
from model.src.database_handler import Database_handler
from model.src.Orms import *
from model.src.API_Grabber import *
from model.src.data_formatter import Data_Formatter

class API_Model(model):
    modes = {
        "vacancy" : 0,
        "area" : 1
    }

    async def refresh_tables(self):
        db_handler = Database_handler()
        await db_handler.drop_table(SalaryOrm.__table__)
        await db_handler.drop_table(VacancyOrm.__table__)
        await db_handler.drop_table(EmployerOrm.__table__)
        await db_handler.drop_table(AreaOrm.__table__)
        await db_handler.create_tables()

    def get_API_data(self, mode):
        if mode in self.modes:
            api_grabber = API_Grabber()
            raw_data = api_grabber.get_data(mode)
            formatter = Data_Formatter(raw_data)
            formatted_data = formatter.format(mode)
            return formatted_data
        else:
            raise ValueError("Unsupported mode type")

    async def load_data_into_tables(self, formatted_data):
        db_handler = Database_handler()
        for model in formatted_data:
            for i in range(0, len(formatted_data[model]), 2048):
                await db_handler.insert_into_table(formatted_data[model][i:i+2048])
    
            