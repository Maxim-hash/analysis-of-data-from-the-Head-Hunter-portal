from model.src.requestHandler import *

class RequestController:
    @classmethod
    def is_handler_exists(cls):
        if hasattr(cls, "handlers"):
            return True
        return False

    def handle_request(self, decoded_data):
        if not self.is_handler_exists():
            raise NotImplementedError("handler is not exist")
        for key in self.handlers:
            if key in decoded_data:
                handler = self.handlers[key]
                return handler.proccess(decoded_data)
            
        raise ValueError("Unknown request type.")


class DataRequestController(RequestController):
    def __init__(self, db_handler, api_grabber):
        self.handlers = {
            "vacancy" : VacancyRequestHandler(db_handler, api_grabber),
            "user" : UserRequestHandler(db_handler),
            "journal" : JournalRequestHandler(db_handler),
        }
    
class AuthRequestController(RequestController):
    def __init__(self, db_handler):
        self.handlers = {
            "ip" :RegistryRequestHandler(db_handler),
            "token" :LoginRequestHandler(db_handler),
        }

class ActionRequestController(RequestController):
    def __init__(self, db_handler):
        self.handlers = {
            "database" : DatabaseUpdateRequestHandler(db_handler),
            "new_status" : UserStatusRequestHandler(db_handler),
        }
