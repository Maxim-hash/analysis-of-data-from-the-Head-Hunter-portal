from model.model import *
from model.src.database_handler import Database_handler
from model.src.API_Grabber import *
from model.src.data_formatter import Data_Formatter

class API_Model(model):
    @staticmethod
    def refresh_tables():
        db_handler = Database_handler()
        db_handler.drop_tables()
        db_handler.create_tables()

    @staticmethod
    def get_API_data():
        api_grabber = API_Grabber()
        raw_data = api_grabber.get_data(5)
        formatter = Data_Formatter(raw_data)
        formatted_data = formatter.format()
    
        return formatted_data
    
    @staticmethod
    def load_data_into_tables(formatted_data):
        db_handler = Database_handler()
        db_handler.insert_into_table(formatted_data)
    
            