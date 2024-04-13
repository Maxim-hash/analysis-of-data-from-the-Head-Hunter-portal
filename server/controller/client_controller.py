from controller.controller import controller
from model.client_model import client_model

class client_controller(controller):
    @staticmethod
    def handle(data):
        splitted_data = data.split(" ")

        if splitted_data[0] == "auth":
            result = client_model.auth(splitted_data[1])
            return result
        elif splitted_data[0] == "get":
            result = client_model.get(splitted_data[1])
            return result
        else:
            return "Incorrect Data"