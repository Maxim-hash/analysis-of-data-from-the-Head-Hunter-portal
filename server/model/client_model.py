import asyncio
import model
from model.src.database_handler import *
import base64

class client_model():
    @staticmethod
    def handle(data):
        return(f"{data} WAS HANDELED")
    
    @staticmethod
    async def auth(data, ip):
        cleaned_string = data.replace("b'", "").replace("'", "")
        decoded = base64.b64decode(cleaned_string).decode()
        login, password = decoded.split(":")
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, login)
        if user == None:
            userObj = UserOrm(email=login, ip=ip, password=password, mode_id=0)
            await db_handler.add(userObj)
            return "200"
        
        return "101"

    @staticmethod
    async def login(data):
        cleaned_string = data.replace("b'", "").replace("'", "")
        decoded = base64.b64decode(cleaned_string).decode()
        login, password = decoded.split(":")
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, login)
        if user == None:
            return "102"
        
        return "200"

    @staticmethod
    def get(data):
        pass