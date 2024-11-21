import asyncio
import jwt
from config import secret_key
from model.src.requestController import ActionRequestController, AuthRequestController, DataRequestController


class DataService:
    def __init__(self, db_handler, api_grabber):
        self.secret_key = secret_key
        self.request_controllers = {
            "auth" : AuthRequestController(db_handler),
            "data" : DataRequestController(db_handler, api_grabber),
            "action" : ActionRequestController(db_handler),
        }

    def get(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, self.secret_key, algorithms=["HS256"])

        if data["role"] == 3:
            return {
                "status": "Denied",
                "data": "Banned User"
            }

        try:
            response = self.request_controllers["data"].handle_request(decoded_data)
            return response
        except ValueError as e:
            return {
                "status": "Error",
                "data": str(e)
            }

    def auth(self, decoded_data):
        try:
            response = asyncio.run(self.request_controllers["auth"].handle_request(decoded_data))
            return response
        except ValueError as e:
            return {
                "status": "Error",
                "data": str(e)
            }

    def action(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if data["role"] == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = "Banned User"

        try:
            response = self.request_controllers["action"].handle_request(decoded_data)
            return response
        except ValueError as e:
            return {
                "status": "Error",
                "data": str(e)
            }
