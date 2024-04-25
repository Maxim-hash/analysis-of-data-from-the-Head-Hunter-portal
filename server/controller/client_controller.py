import asyncio
from controller.controller import controller
from model.client_model import client_model 

class client_controller(controller):
    @staticmethod
    def handle(ip, data):
        model = client_model()
        splitted_data = data.split(" ")

        if splitted_data[0] == "auth": 
            result = asyncio.run(model.auth(splitted_data[1], ip))
        elif splitted_data[0] == "login":
            result = asyncio.run(model.login(splitted_data[1]))
        elif splitted_data[0] == "get":
            result = model.get(splitted_data[1])
        else:
            result = "Incorrect Data"
        
        return result