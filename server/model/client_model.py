import asyncio
import functools
import model
from model.src.database_handler import *
import base64

class client_model():
    def __init__(self) -> None:
        self.return_code = {
            "Access" : "20",
            "Denied" : "10" 
            }
        
    def parse_credentials(func):
        @functools.wraps(func)
        async def wrapper(cls, data, *args, **kwargs):
            cleaned_string = data.replace("b'", "").replace("'", "")
            decoded = base64.b64decode(cleaned_string).decode()
            login, password = decoded.split(":")
            return await func(cls, login, password, *args, **kwargs)
        return wrapper
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")
    
    @parse_credentials
    async def auth(self, login, password, ip):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, login)
        if user == None:
            userObj = UserOrm(email=login, ip=ip, password=password, mode_id=0)
            await db_handler.add(userObj)
            return self.return_code["Access"] + "0"
        
        return self.return_code["Denied"] + "1"

    @parse_credentials
    async def login(self, login, password):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, login)
        if user == None:
            self.return_code["Denied"] + "2"
            
        return self.return_code["Access"] + "0"


    def get(self, data):
        pass