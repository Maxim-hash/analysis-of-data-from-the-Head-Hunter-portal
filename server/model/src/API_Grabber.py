from copy import deepcopy
from datetime import datetime, timedelta
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

class API_Grabber():
    def __init__(self, per_page=100):
        self.base_url = "https://api.hh.ru"
        self.per_page = per_page
        generator = DateIntervalGenerator()
        self.hour_interval = generator.generate_hour_intervals()
        self.mode_types = ["area", "vacancy"]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }

    def get_pagination(self, url):
        raw_response = requests.get(url, timeout=5)
        while raw_response.status_code == 403:
            time.sleep(10)
            raw_response = requests.get(url, timeout=5)
        response = raw_response.json()
        pagination = response['found'] // self.per_page + 1
        return pagination

    def fetch_page(self, url):
        session = requests.Session()

        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            response = session.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def prepare_request(self, mode):
        urls = []
        params = []
        if mode == "area":
            url = URL_creator(mode, self.base_url)
            urls.append(url.build_url())
            return urls
        
        for interval in self.hour_interval:
            for page in range(0, 19):
                params = {
                    'date_from': interval["date_from"],
                    'date_to': interval["date_to"],
                    'per_page': self.per_page,
                    'page': page
                }
                url = URL_creator(mode, self.base_url, params)
                urls.append(url.build_url())
        return urls

    def get_data(self, mode, count = -1):
        if mode in self.mode_types:
            collected_data = []
            
            urls = self.prepare_request(mode)
            for url in urls:
                if count != -1 and len(collected_data) > count:
                    break
                response = self.fetch_page(url)
                if type(response) == list:
                    collected_data.extend(response)
                elif response:
                    collected_data.extend(response.get('items', []))
                    if len(response.get('items', [])) < self.per_page:
                        break  # Нет больше страниц

            return collected_data
        else:
            raise ValueError("Unsupported mode type")

class URL:
    def __init__(self, url) -> None:
        self.url = url

    def add_path(self, path):
        self.url += f"/{path}"

    def __str__(self) -> str:
        return self.url

    def get_url(self):
        return self.url

class Dynamic_URL(URL):
    def __init__(self, url, items = None) -> None:
        super().__init__(url)
        self.items = ""
        if items:
            self.add_item(items)
        
    def add_item(self, items):
        self.items += "".join(f"&{i}={items[i]}" for i in items)

    def __str__(self):
        return f"{self.url}?{self.items}"

class Static_URL(URL):
    def __init__(self, url, params = None) -> None:
        super().__init__(url)
        if params:
            self.add_path(params)

class Area_URL(Static_URL):
    def __init__(self, url, params = None) -> None:
        super().__init__(f"{url}/areas", params)

class Vacancy_URL(Dynamic_URL):
    def __init__(self, url, params = None) -> None:
        super().__init__(f"{url}/vacancies", params)

class URL_creator:
    url_types = {
            "area": Area_URL,
            "vacancy": Vacancy_URL
        }
    
    def __init__(self, url_class, *args):
        self.url_class = self._get_url_class(url_class)
        self.url_instance = self.url_class(*args)

    def _get_url_class(self, url_type):
        if url_type in self.url_types:
            return self.url_types[url_type]
        else:
            raise ValueError("Unsupported URL type")

    def build_url(self):
        return self.url_instance
    
    def add_items(self, items):
        self.url_instance.add_item(items)
    
class DateIntervalGenerator:
    def __init__(self):
        self.today = datetime.today()
        self.one_month_ago = self.today - timedelta(days=30)

    def generate_hour_intervals(self):
        intervals = []
        current_start_date = self.one_month_ago
        while current_start_date < self.today:
            current_end_date = current_start_date + timedelta(hours=1)  # Интервал в один час
            intervals.append({
                'date_from': current_start_date.isoformat(),
                'date_to': current_end_date.isoformat()
            })
            current_start_date += timedelta(hours=1)
        return intervals
    

def rec(b, buffer = []):
    if not b["areas"]:
        return (b["id"], b["parent_id"], b["name"])
    for i in b["areas"]:
        buffer.append(rec(i))
    return buffer

if __name__ == "__main__":
    a = URL_creator("vacancy", "https://api.hh.ru", {123145: "qwe", "qweqrq":"eqwr12441", "qqwrq":"eqwr12441"})
    b = URL_creator("area", "https://api.hh.ru", 12312)
    c = URL_creator("vacancy", a.build_url())
    print(a.build_url())
    print(b.build_url())
    print(c.build_url())

#    b = a.fetch()
#    temp = []
#    for i in b:
#        temp.append((i["id"], i["parent_id"], i["name"]))
#        temp.extend(rec(i)[-1])
#        print(temp)