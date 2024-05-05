import jwt
import json
from model.src.database_handler import *
from config import secret_key
from datetime import datetime

class ClientModel():
    def __init__(self) -> None:
        self.return_data = {
            "statues" : None,
            "data" : None
        }
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")

    async def auth(self, decoded_data, ip):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])
        if user == None and decoded_data["password"]:
            
            payloads = {
                'role' : 0,
                'exp': datetime.today()
            }
            token = jwt.encode(payloads, secret_key, algorithm="HS256")
            userObj = UserOrm(email=decoded_data["login"], ip=ip, password=decoded_data["password"], token=token, mode_id=0)
            await db_handler.add(userObj)
            self.return_data["status"] = "Access"
            self.return_data["data"] = token
            return json.dumps(self.return_data)
        
        self.return_data["status"] = "Denied"
        self.return_data["data"] = 'Invalid username'
        return json.dumps(self.return_data)

    async def login(self, decoded_data):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])

        if user == None:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = 'Invalid username'
            return json.dumps(self.return_data)
        
        if user.mode_id == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = 'Invalid username'
            return json.dumps(self.return_data)
        
        if decoded_data["password"] == user.password:
            payload = {
                "role" : user.mode_id,
                "exp" : datetime.today()
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            self.return_data["status"] = "Access"
            self.return_data["data"] = token
            return json.dumps(self.return_data)
        
        self.return_data["status"] = "Denied"
        self.return_data["data"] = "Untrackable error"
        return json.dumps(self.return_data)

    def get(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if data["role"] == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = "Banned User"
            return json.dumps(self.return_data)
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
        self.return_data["status"] = "Access"
        self.return_data["data"] = answer
        return json.dumps(self.return_data)
    
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
        return int(sal / self.exchange[cur])

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