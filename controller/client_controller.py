from controller.controller import controller
from model.client_model import client_model

class client_controller(controller):
    @staticmethod
    def handle(data):
        if data:
            result = client_model.handle(data)
            return result
        else:
            return "Incorrect Data"