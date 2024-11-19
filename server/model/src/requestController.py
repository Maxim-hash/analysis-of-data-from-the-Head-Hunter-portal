from model.src.requestHandler import VacancyRequestHandler, UserRequestHandler, JournalRequestHandler

class RequestController:
    @classmethod
    def is_exists_handler(cls):
        if hasattr(cls, "handlers"):
            return True
        return False

    def handle_request(self, decoded_data):
        if not self.is_exists_handler():
            raise NotImplementedError("handler is not exist")
        for key in self.handlers:
            if key in decoded_data:
                handler = self.handlers[key]
                return handler.proccess(decoded_data)
            
        raise ValueError("Unknown request type.")


class DataRequestController(RequestController):
    def __init__(self, db_handler, api_grabber):
        self.handlers = {
            "vacancy" : VacancyRequestHandler(db_handler),
            "user" : UserRequestHandler(db_handler),
            "journal" : JournalRequestHandler(db_handler, api_grabber),
        }
    
class AuthRequestController(RequestController):
    def __init__(self):
        self.handlers = {
            ...
        }

class ActionRequestController(RequestController):
    def __init__(self):
        self.handlers = {
            ...
        }
