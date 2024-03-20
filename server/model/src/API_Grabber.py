import requests

class API_Grabber():
    def __init__(self, per_page = 100) -> None:
        self.url = f"https://api.hh.ru/vacancies?per_page={per_page}"
        self.per_page = per_page
        response = requests.get(self.url).json()
        self.quantity_pagination = round(response['found'] / self.per_page, 0) + 1

    def get_data(self, count = -1):
        size = count if count else self.quantity_pagination
        data = list()
        page = 0
        while page <= size:
            response = requests.get(self.url, timeout=5).json()
            data.append(response)
            page += 1

        return data
    