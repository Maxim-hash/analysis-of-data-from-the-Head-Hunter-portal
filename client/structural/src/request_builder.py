import base64
import json

class RequestTemplate:
    def __init__(self, action : str, **kwargs) -> None:
        self.action = action
        self.params = kwargs

    def get_template(self):
        return {
            "action" : self.action,
            **self.params
        }
    
class LoginRequestTemplate(RequestTemplate):
    def __init__(self, login = "login", password = "password") -> None:
        super().__init__("login", login=login, password=password)
    
class AuthRequestTemplate(RequestTemplate):
    def __init__(self, login = "login", password = "password") -> None:
        super().__init__("auth", login=login, password=password)
    
class GetRequestTemplate(RequestTemplate):
    def __init__(self, vacancy_name = "", area = "", exp = "%") -> None:
        super().__init__("get", vacancy_name=vacancy_name, area=area, exp=exp)
    
class JSONRequestBuilder:
    def __init__(self, templateRequest: RequestTemplate):
        self.request_data = templateRequest.get_template()

    def build(self):
        return json.dumps(self.request_data)