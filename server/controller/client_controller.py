import asyncio
import json
from controller.controller import controller
from model.client_model import ClientModel 

class client_controller(controller):
    @staticmethod
    def handle(ip, data: dict):
        converter = {
            "Access" : True,
            "Denied" : False
        }
        model = ClientModel()
        needed_data = {key : value for key, value in data.items() if key != "action"}
        
        if data['action'] == "auth": 
            needed_data['ip'] = ip
            result = asyncio.run(model.auth(needed_data, ip))
        elif data['action'] == "login":
            result = asyncio.run(model.login(needed_data))
        elif data['action'] == "get":
            result = model.get(needed_data)
        elif data["action"] == "update":
            result = model.update(needed_data)
        else:
            result = "Incorrect Data"
        if "token" in data and "journal" not in data and "user" not in data:
            logging_data = {key : value for key, value in data.items() if key != "token"}
            asyncio.run(model.logging(data["token"], str(logging_data), converter[result['status']]))

        return json.dumps(result)