import base64

class Requst_Builder:
    def __init__(self, mode):
        if mode == "auth":
            self.request = Auth_request()
        elif mode == "get":
            self.request = Get_request()
        elif mode == "login":
            self.request = Login_requset()

    def add_item(self, items):
        if hasattr(items, "__iter__") and not isinstance(items, str):
            self.request.body.extend(items)
        else:
            self.request.body.append(items)

    def build(self):
        payloads = base64.b64encode(':'.join(self.request.body).encode())

        return f"{self.request.name} {payloads}" 

class request:
    def __init__(self, name) -> None:
        self.name = name
        self.body = []

class Login_requset(request):
    def __init__(self) -> None:
        super().__init__("login")

class Auth_request(request):
    def __init__(self) -> None:
        super().__init__("auth")

class Get_request(request):
    def __init__(self) -> None:
        super().__init__("get")