from controller.controller import controller
from model.api_model import API_Model

class api_controller(controller):
    @staticmethod
    def update_database():
        #API_Model.refresh_tables()
        data = API_Model.get_API_data()

        #return data
