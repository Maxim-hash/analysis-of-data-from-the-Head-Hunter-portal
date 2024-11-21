import asyncio
import jwt
import json
from model.src.dataService import DataService
from model.src.database_handler import *
from controller.api_controller import *
from model.src.API_Grabber import *
from config import secret_key
from datetime import datetime

from model.src.utils import get_salary

class ClientModel():
    def __init__(self) -> None:
        db_handler = Database_handler()
        api_grabber = API_Grabber()
        self.data_service = DataService(db_handler, api_grabber)
        self.return_data = {}
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")

    async def auth(self, decoded_data):
        self.return_data = await self.data_service.auth(decoded_data)
        return self.return_data

    def get(self, decoded_data):
        self.return_data = self.data_service.get(decoded_data)
        return self.return_data
    
    def update(self, decoded_data):
        self.return_data = self.data_service.action(decoded_data)
        return self.return_data

    async def logging(self, token, action, status):
        user_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        db_handler = Database_handler()
        journal_entry = JournalOrm(token=user_token["login"], action=action, status=status, time= datetime.today())
        await db_handler.add(journal_entry)
