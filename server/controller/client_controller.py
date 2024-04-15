import asyncio
from controller.controller import controller
from model.client_model import client_model

class client_controller(controller):
    @staticmethod
    def handle(ip, data):
        splitted_data = data.split(" ")

        if splitted_data[0] == "auth":
            result = asyncio.run(client_model.auth(splitted_data[1], ip))
        elif splitted_data[0] == "login":
            result = asyncio.run(client_model.login(splitted_data[1]))
        elif splitted_data[0] == "get":
            result = client_model.get(splitted_data[1], ip)
        else:
            result = "Incorrect Data"
        
        return result