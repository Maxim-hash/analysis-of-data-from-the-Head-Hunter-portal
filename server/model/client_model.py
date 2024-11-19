import asyncio
import jwt
import json
from model.src.database_handler import *
from controller.api_controller import *
from model.src.API_Grabber import *
from config import secret_key
from datetime import datetime

from model.src.utils import get_salary

class ClientModel():
    def __init__(self) -> None:
        self.return_data = {
            "status" : None,
            "data" : None
        }
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")

    async def auth(self, decoded_data, ip):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])
        if user == None and decoded_data["password"]:
            
            payloads = {
                'login' : decoded_data["login"],
                'role' : 0,
                'exp': datetime.today()
            }
            token = jwt.encode(payloads, secret_key, algorithm="HS256")
            userObj = UserOrm(email=decoded_data["login"], ip=ip, password=decoded_data["password"], token=token, mode_id=0)
            await db_handler.add(userObj)
            self.return_data["status"] = "Access"
            self.return_data["data"] = token
            return self.return_data
        
        self.return_data["status"] = "Denied"
        self.return_data["data"] = 'Invalid username'
        return self.return_data

    async def login(self, decoded_data):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data["login"])

        if user == None:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = 'User is not registered'
            return self.return_data
        
        if user.mode_id == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = 'Banned user'
            return self.return_data
        
        if decoded_data["password"] == user.password:
            payload = {
                'login' : user.email,
                "role" : user.mode_id,
                "exp" : datetime.today()
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            self.return_data["status"] = "Access"
            self.return_data["data"] = token
            return self.return_data
        
        self.return_data["status"] = "Denied"
        self.return_data["data"] = "Invalid password"
        return self.return_data

    def get(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if data["role"] == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = "Banned User"
            return self.return_data
        db_handler = Database_handler()
        if "journal" in decoded_data:
            result = db_handler.select(decoded_data, JournalOrm)
            data = {}
            for i in result:
                obj = {**(i.__dict__)}
                obj.pop('_sa_instance_state', None)
                data[obj['id']] = obj.copy()
                data[obj['id']]["time"] = data[obj['id']]["time"].isoformat() 
                data[obj['id']].pop("id", None)
            self.return_data["status"] = "Access"
            self.return_data["data"] = data
            return self.return_data
        if "user" in decoded_data:
            result = db_handler.select(decoded_data, UserOrm)
            data = {}
            for i in result:
                obj = {**(i.__dict__)}
                obj.pop('_sa_instance_state', None)
                data[obj['email']] = obj.copy()
                data[obj['email']].pop("email", None)
            self.return_data["status"] = "Access"
            self.return_data["data"] = data
            return self.return_data
        result = db_handler.select(decoded_data, VacancyOrm)
        grabber = API_Grabber()
        salary = []
        
        ids = [item.id for item in result]
        dictionarys = grabber.get_skills_data(ids)
        skills = dict(zip(ids, dictionarys))
        for i in skills:
            if data:  # Проверка на пустоту массива
                names = [item['name'] for item in skills[i]]
            else:
                names = []
            skills[i] = {"key_skills" : names}
        for item in result:
            salary.extend(db_handler.select(item, SalaryOrm))
            
        
        result_salary = get_salary(salary)
        answer = {}
        for item_vac, item_sal, item_skill in zip(result, result_salary, skills):
            object = {**(item_vac.__dict__), **item_sal, **skills[item_skill]}
            object.pop('_sa_instance_state', None)
            answer[f"{object['id']}"] = object.copy()
            answer[f"{object['id']}"].pop("id", None)
        self.return_data["status"] = "Access"
        self.return_data["data"] = answer
        return self.return_data
    
    def update(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if data["role"] == 3:
            self.return_data["status"] = "Denied"
            self.return_data["data"] = "Banned User"
            return self.return_data
        db_handler = Database_handler()
        if "new_password" in decoded_data:
            db_handler.update_password(decoded_data["username"], decoded_data["new_password"])
            self.return_data["status"] = "Access"
            self.return_data["data"] = "Password has been changed"

        elif "new_status" in decoded_data:
            user = asyncio.run(db_handler.get(UserOrm, decoded_data["username"]))
            if user.mode_id == 2:
                self.return_data["status"] = "Denied"
                self.return_data["data"] = "This user admin"

            db_handler.update_user_status(decoded_data["username"], decoded_data["new_status"])
            self.return_data["status"] = "Access"
            self.return_data["data"] = "Status has been changed"

        elif "database" in decoded_data:
            asyncio.run(api_controller.update_database())
            self.return_data["status"] = "Access"
            self.return_data["data"] = "Database has been updated"
        return self.return_data

    async def logging(self, token, action, status):
        user_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        db_handler = Database_handler()
        journal_entry = JournalOrm(token=user_token["login"], action=action, status=status, time= datetime.today())
        await db_handler.add(journal_entry)
