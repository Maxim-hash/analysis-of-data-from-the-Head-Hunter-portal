from config import secret_key


class DataService:
    def __init__(self):
        self.secret_key = secret_key
        self.request_controller = RequestContoller()
