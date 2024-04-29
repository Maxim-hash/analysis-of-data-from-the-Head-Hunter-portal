import asyncio
import functools
import json
import model
from model.src.database_handler import *
import base64

class ClientModel():
    def __init__(self) -> None:
        self.return_code = {
            "Access" : "20",
            "Denied" : "10" 
            }
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")

    async def auth(self, decoded_data, ip):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])
        if user == None:
            userObj = UserOrm(email=decoded_data["login"], ip=ip, password=decoded_data["password"], mode_id=0)
            await db_handler.add(userObj)
            return self.return_code["Access"] + "0"
        
        return self.return_code["Denied"] + "1"

    async def login(self, decoded_data):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])
        if user == None:
            return self.return_code["Denied"] + "2"

        return self.return_code["Access"] + "0"

    def get(self, decoded_data):
        db_handler = Database_handler()
        result = db_handler.select(decoded_data, "Vacancy")
        result_salary = []
        for item in result:
            result_salary.extend(db_handler.select(item, "Salary"))
        answer = {}
        for item_vac, item_sal in zip(result, result_salary):
            object = {**(item_vac.__dict__), **(item_sal.__dict__)}
            object.pop('_sa_instance_state', None)
            answer[f"{object['id']}"] = object.copy()
            answer[f"{object['id']}"].pop("id", None)
        if len(answer) == 0:
            answer["202"] = "None"
        return json.dumps(answer)