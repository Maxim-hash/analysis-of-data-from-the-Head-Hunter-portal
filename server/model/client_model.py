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

    async def get(self, decoded_data):
        db_handler = Database_handler()
        result = db_handler.select(decoded_data, "Vacancy")
        salary = []
        for item in result:
            salary.extend(db_handler.select(item, "Salary"))
        
        result_salary = get_salary(salary)
        answer = {}
        for item_vac, item_sal in zip(result, result_salary):
            object = {**(item_vac.__dict__), **item_sal}
            object.pop('_sa_instance_state', None)
            answer[f"{object['id']}"] = object.copy()
            answer[f"{object['id']}"].pop("id", None)
        if len(answer) == 0:
            answer["202"] = "None"
        return json.dumps(answer)
    
class СurrencyConverter:
    def __init__(self) -> None:
        self.exchange = {
            "AZN" : 0.0186,
            "BYR" : 0.0356,
            "EUR" : 0.0102,
            "GEL" : 0.0291,
            "KGS" : 0.968,
            "KZT" : 4.82,
            "RUR" : 1,
            "UAH" : 0.431,
            "USD" : 0.0109,
            "UZS" : 136.87,
        }
        
    def convert(self, sal : int, cur : str):
        return int(sal * self.exchange[cur])

def get_salary(salary_ORM_list: List[SalaryOrm]):
    result = []
    conveter = СurrencyConverter()
    for i in salary_ORM_list:
        if i.s_from == None:
            result.append({"salary" : None})
            continue
        if i.s_to == None:
            result.append({"salary" : i.s_from})
            continue
        sum = conveter.convert((i.s_from + i.s_to) / 2, i.currency)
        result.append({"salary" : sum})

    return result