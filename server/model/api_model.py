from model.model import *
from model.src.database_handler import Database_handler
from model.src.API_Grabber import *
from model.src.data_formatter import Data_Formatter
import asyncio

class API_Model(model):
    @staticmethod
    def refresh_tables():
        db_handler = Database_handler()
        db_handler.drop_tables()
        db_handler.create_tables()

    @staticmethod
    def get_API_data():
        api_grabber = API_Grabber()
        raw_data = api_grabber.get_data()
        formatter = Data_Formatter(raw_data)
        temp = 0
        for i in raw_data:
            temp += len(i)
        formatted_data = formatter.format()
        return raw_data
    
            