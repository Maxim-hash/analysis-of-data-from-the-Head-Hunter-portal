from controller.controller import controller
from model.api_model import API_Model

class api_controller(controller):
    @staticmethod
    def update_database():
        api_model = API_Model()
        api_model.refresh_tables()
        formatted_data = api_model.get_API_data("area")
        api_model.load_data_into_tables(formatted_data)
        formatted_data = api_model.get_API_data("vacancy")
        api_model.load_data_into_tables(formatted_data)
        #return data
