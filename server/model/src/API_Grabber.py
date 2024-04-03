from datetime import datetime, timedelta
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

class API_Grabber():
    def __init__(self, per_page=100):
        self.base_url = "https://api.hh.ru/vacancies"
        self.per_page = per_page
        generator = DateIntervalGenerator()
        self.hour_interval = generator.generate_hour_intervals()

    def get_pagination(self, url):
        raw_response = requests.get(url, timeout=5)
        while raw_response.status_code == 403:
            time.sleep(10)
            raw_response = requests.get(url, timeout=5)
        response = raw_response.json()
        pagination = response['found'] // self.per_page + 1
        return pagination

    def fetch_page(self, params):
        ext = "".join(f"&{i}={params[i]}" for i in params)
        url = f"{self.base_url}?{ext}"
        headers = {"User-Agent": "Mediapartners-Google"}
        session = requests.Session()

        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            response = session.get(url, headers=headers, timeout=5)
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

    def get_data_for_date_interval(self, date_from, date_to):
        url = f"{self.base_url}?&date_from={date_from}&date_to={date_to}"
        pagination = self.get_pagination(url)
        collected_data = []
        if pagination >= 20:
            pagination = 19
        for page in range(0, pagination):
            params = {
                'date_from': date_from,
                'date_to': date_to,
                'per_page': self.per_page,
                'page': page
            }
            response = self.fetch_page(params)
            if response:
                collected_data.extend(response.get('items', []))
                if len(response.get('items', [])) < self.per_page:
                    break  # Нет больше страниц
        return collected_data

    def get_data(self, count = -1):
        response = []
        for interval in self.hour_interval:
            if count != -1 and len(response) > count:
                break
            response.append(self.get_data_for_date_interval(interval["date_from"], interval["date_to"]))

        return response

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