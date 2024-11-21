import asyncio
from datetime import datetime

import jwt
from model.src.API_Grabber import *
from model.src.Orms import JournalOrm, SalaryOrm, UserOrm, VacancyOrm
from model.src.database_handler import Database_handler
from model.src.utils import get_salary
from config import secret_key
from controller import api_controller


class RequestHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.answer = {
            "status" : "Denied",
        }

    @classmethod
    def is_user_is_admin(cls, userRole):
        if userRole == 2:
            return True
        return False

    @classmethod
    def is_user_exists(cls, user):
        if user:
            return True
        return False

    @classmethod
    def is_user_banned(cls, userRole):
        if userRole == 3:
            return True
        return False
    
    @classmethod
    def is_user_not_registrated(cls, user, password):
        if user == None and password:
            return True
        return False

    def proccess(self, decoded_data):
        raise NotImplementedError("This method should be implemented in a subclass")
    

class VacancyRequestHandler(RequestHandler):
    def __init__(self, db_handler, api_grabber):
        self.api_grabber = api_grabber
        super().__init__(db_handler)

    def proccess(self, decoded_data):
        result = self.db_handler.select(decoded_data, VacancyOrm)
        postproccess_data = {}
        ids = [item.id for item in result]
        skills_data = self.api_grabber.get_skills_data(ids)
        skills = {vacancy_id : {"key_skills" : [skill["name"] for skill in skills_data[vacancy_id]]} for vacancy_id in ids}

        salary = []
        for item in result:
            salary.extend(self.db_handler.select(item, SalaryOrm))
        result_salary = get_salary(salary)

        for item_vac, item_sal, item_skill in zip(result, result_salary, skills):
            object = {**(item_vac.__dict__), **item_sal, **skills[item_skill]}
            object.pop('_sa_instance_state', None)
            postproccess_data[f"{object['id']}"] = object.copy()
            postproccess_data[f"{object['id']}"].pop("id", None)
        self.answer["data"] = postproccess_data

        return self.answer
    
class JournalRequestHandler(RequestHandler):
    def proccess(self, decoded_data):
        result = self.db_handler.select(decoded_data, JournalOrm)
        postproccess_data = {}
        
        for i in result:
            obj = {**(i.__dict__)}
            obj.pop('_sa_instance_state', None)
            postproccess_data[obj['id']] = obj.copy()
            postproccess_data[obj['id']]["time"] = postproccess_data[obj['id']]["time"].isoformat() 
            postproccess_data[obj['id']].pop("id", None)
        self.answer["data"] = postproccess_data

        return self.answer
    
class UserRequestHandler(RequestHandler):
    def proccess(self, decoded_data):
        result = self.db_handler.select(decoded_data, UserOrm)
        postproccess_data = {}

        if self.is_user_banned(decoded_data["role"]):
            self.answer["data"] = "Banned User"
            return self.answer
        
        for i in result:
            obj = {**(i.__dict__)}
            obj.pop('_sa_instance_state', None)
            postproccess_data[obj['email']] = obj.copy()
            postproccess_data[obj['email']].pop("email", None)

        self.answer["status"] = "Access"
        self.anser["data"] = postproccess_data
        
        return self.answer
    
class LoginRequestHandler(RequestHandler):
    async def proccess(self, decoded_data):
        user = await self.db_handler.get(UserOrm, decoded_data["login"])

        if self.is_user_banned(user.mode_id):
            self.answer["data"] = 'User is Banned'
            return self.answer

        if self.is_user_exists(user):
            self.answer["data"] = 'User is not registered'
            return self.answer
        
        if decoded_data["password"] == user.password:
            payload = {
                'login' : user.email,
                "role" : user.mode_id,
                "exp" : datetime.today()
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")

            self.answer["data"] = token
            self.answer["status"] = "Access"

            return self.answer

        self.answer["data"] = "Invalid password"

        return self.answer

class RegistryRequestHandler(RequestHandler):
    async def proccess(self, decoded_data):
        user = await self.db_handler.get(UserOrm, decoded_data["login"])

        if self.is_user_not_registrated(user, decoded_data["password"]):
            
            payloads = {
                'login' : decoded_data["login"],
                'role' : 0,
                'exp': datetime.today()
            }
            token = jwt.encode(payloads, secret_key, algorithm="HS256")
            userObj = UserOrm(email=decoded_data["login"], ip=decoded_data["ip"], password=decoded_data["password"], token=token, mode_id=0)
            await self.db_handler.add(userObj)

            self.answer["data"] = token
            self.answer["status"] = "Access"

            return self.answer
        
        self.answer["data"] = 'Invalid username'

        return self.answer

class DatabaseUpdateRequestHandler(RequestHandler):
    def proccess(self, decoded_data):
        token = decoded_data["token"]
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        if self.is_user_is_admin(data["role"]):
            self.answer["data"] = "It is not a admin"
            return self.answer
        
        asyncio.run(api_controller.update_database())
        
        self.answer["data"] = "Database has been updated"
        self.answer["status"] = "Access"

        return self.answer

class UserStatusRequestHandler(RequestHandler):
    def proccess(self, decoded_data):  
        user = asyncio.run(self.db_handler.get(UserOrm, decoded_data["username"]))
        if self.is_user_is_admin(user):
            self.answer["data"] = "This user admin"
            return self.answer

        self.db_handler.update_user_status(decoded_data["username"], decoded_data["new_status"])

        self.answer["data"] = "Status has been changed"
        self.answer["status"] = "Access"

        return self.answer

class ChangePasswordRequestHandler(RequestHandler):
    def proccess(self, decoded_data):
        self.db_handler.update_password(decoded_data["username"], decoded_data["new_password"])
        
        self.answer["data"] = "Password has been changed"
        self.answer["status"] = "Access"

        return self.answer
