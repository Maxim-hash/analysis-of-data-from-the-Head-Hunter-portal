from model.model import *
from model.src.database_handler import Database_handler
from model.src.API_Grabber import *

class API_Model(model):
    @staticmethod
    def refresh_tables():
        db_handler = Database_handler()
        db_handler.drop_tables()
        db_handler.create_tables()

    @staticmethod
    def get_API_data():
        api_grabber = API_Grabber()
        api_grabber.set_quantity_pagination()
        data = api_grabber.get_data()
        return data
    
            