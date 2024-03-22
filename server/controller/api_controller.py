from controller.controller import controller
from model.api_model import API_Model

class api_controller(controller):
    @staticmethod
    def update_database():
        API_Model.refresh_tables()
        formatted_data = API_Model.get_API_data()
        API_Model.load_data_into_tables(formatted_data)
        #return data
