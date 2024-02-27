from controller.controller import controller
from model.api_model import api_model

class api_controller(controller):
    @staticmethod
    def update_database():
        #data = api_model.get_API_data()
        api_model.create_tables()
        #api_model.drop_database()
        api_model.update_database()
        #return data
