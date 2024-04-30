import asyncio
from controller.controller import controller
from model.client_model import ClientModel 

class client_controller(controller):
    @staticmethod
    def handle(ip, data: dict):
        model = ClientModel()
        needed_data = {key : value for key, value in data.items() if key != "action"}
        if data['action'] == "auth": 
            result = asyncio.run(model.auth(needed_data, ip))
        elif data['action'] == "login":
            result = asyncio.run(model.login(needed_data))
        elif data['action'] == "get":
            result = asyncio.run(model.get(needed_data))
        else:
            result = "Incorrect Data"
        
        return result