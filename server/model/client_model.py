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
        
    def parse_input(func):
        @functools.wraps(func)
        def wrapper(self, *args):
            input_string = args[0]
            cleaned_string = input_string.replace("b'", "").replace("'", "")
            decoded = base64.b64decode(cleaned_string).decode()
            split_input = decoded.split(":")

            return func(self, split_input, *args[1:])
        return wrapper
        
    def handle(self, data):
        return(f"{data} WAS HANDELED")
    
    @parse_input
    async def auth(self, decoded_data, ip):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data[0])
        if user == None:
            userObj = UserOrm(email=decoded_data[0], ip=ip, password=decoded_data[1], mode_id=0)
            await db_handler.add(userObj)
            return self.return_code["Access"] + "0"
        
        return self.return_code["Denied"] + "1"

    @parse_input
    async def login(self, decoded_data):
        db_handler = Database_handler()
        user = await db_handler.get(UserOrm, decoded_data[0])
        if user == None:
            return self.return_code["Denied"] + "2"

        return self.return_code["Access"] + "0"

    @parse_input
    def get(self, decoded_data):
        db_handler = Database_handler()
        result = db_handler.select(decoded_data)
        result_string = ""
        for item in result:
            result_string += f"{item.id}:{item.name}:{item.exp}:{item.empoyment},"
        if len(result_string) == 0:
            result_string = "None"
        return result_string