from copy import deepcopy
from datetime import datetime, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import aiohttp
import asyncio
from config import HEADERS

class API_Grabber():
    def __init__(self, per_page=100):
        self.base_url = "https://api.hh.ru"
        self.per_page = per_page
        generator = DateIntervalGenerator()
        self.hour_interval = generator.generate_hour_intervals()
        self.mode_types = ["area", "vacancy"]
        self.headers = HEADERS

    async def fetch_page(self, url):
        #session = requests.Session()

        #retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 403, 500, 502, 503, 504])
        #session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(str(url)) as response:
                    response.raise_for_status()  # Проверка на ошибки HTTP
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                print(f"Ошибка: {e.status}, Сообщение: {e.message}, URL: {e.request_info.url}")
            else:
                print(f"Ошибка HTTP: {e.status}, URL: {e.request_info.url}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    async def fetch_vacancy_data(self, url, session, data):
        try:
            async with session.get(str(url)) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                temp = await response.json()
                data.append(temp["key_skills"])
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                print(f"Ошибка: {e.status}, Сообщение: {e.message}, URL: {e.request_info.url}")
            else:
                print(f"Ошибка HTTP: {e.status}, URL: {e.request_info.url}")
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
        except asyncio.TimeoutError as e:
            print(f"Timeout error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    async def get_skills(self, urls):
        data = []

        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [self.fetch_vacancy_data(url, session, data) for url in urls]
            await asyncio.gather(*tasks)
        return data

    def get_skills_data(self, vacancy_ids):
        url = URL_creator("vacancy", self.base_url)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        urls = [f"{url.url_instance.url}/{vacancy_id}" for vacancy_id in vacancy_ids]
        data = loop.run_until_complete(self.get_skills(urls))

        return data
        
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

    async def get_data(self, mode, count = -1):
        if mode in self.mode_types:
            collected_data = []
            
            urls = self.prepare_request(mode)
            for url in urls:
                if count != -1 and len(collected_data) > count:
                    break
                response = await self.fetch_page(url)
                if type(response) == list:
                    collected_data.append(response)
                elif response:
                    collected_data.append(response.get('items', []))
                    if len(response.get('items', [])) < self.per_page:
                        continue  # Нет больше страниц

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
            current_end_date = current_start_date + timedelta(minutes=30)  # Интервал в один час
            intervals.append({
                'date_from': current_start_date.isoformat(),
                'date_to': current_end_date.isoformat()
            })
            current_start_date += timedelta(minutes=35)
        return intervals
