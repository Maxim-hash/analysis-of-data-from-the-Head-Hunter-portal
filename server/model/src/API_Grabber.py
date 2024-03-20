import requests

class API_Grabber():
    def __init__(self, per_page = 100) -> None:
        if per_page > 100:
            return -1
        self.url = f"https://api.hh.ru/vacancies?per_page={per_page}"
        self.per_page = per_page
        response = requests.get(self.url).json()
        self.quantity_pagination = round(response['found'] / self.per_page, 0) + 1

    def get_data(self, count = -1):
        size = count if count != -1 else self.quantity_pagination
        data = list()
        page = 0
        while page < size:
            response = requests.get(self.url, timeout=None, headers={'User-Agent': 'some cool user-agent'}).json()
            data.append(response)
            page += 1

        return data
    