import model
from model.src.database_handler import *
import base64

class client_model():
    @staticmethod
    def handle(data):
        return(f"{data} WAS HANDELED")
    
    @staticmethod
    def auth(data):
        cleaned_string = data.replace("b'", "").replace("'", "")
        decoded = base64.b64decode(cleaned_string).decode()
        login, password = decoded.split(":")
        print(data)

    @staticmethod
    def login(data):
        pass

    @staticmethod
    def get(data):
        pass