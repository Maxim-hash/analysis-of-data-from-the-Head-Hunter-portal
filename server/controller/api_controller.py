from controller.controller import controller
from model.api_model import API_Model

class api_controller(controller):
    @staticmethod
    async def update_database():
        api_model = API_Model()
        await api_model.refresh_tables()
        formatted_data = await api_model.get_API_data("area")
        await api_model.load_data_into_tables(formatted_data)
        formatted_data = await api_model.get_API_data("vacancy")
        await api_model.load_data_into_tables(formatted_data)
        

        return 0
