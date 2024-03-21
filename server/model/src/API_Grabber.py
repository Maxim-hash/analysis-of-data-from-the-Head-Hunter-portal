from datetime import datetime, timedelta
import requests

class API_Grabber():
    def __init__(self, per_page=100):
        self.base_url = "https://api.hh.ru/vacancies"
        self.per_page = per_page
        generator = DateIntervalGenerator()
        self.hour_interval = generator.generate_hour_intervals()

    def get_pagination(self, url):
        response = requests.get(url, timeout=5).json()
        pagination = response['found'] // self.per_page + 1
        return pagination

    def fetch_page(self, params):
        ext = "".join(f"&{i}={params[i]}" for i in params)
        url = f"{self.base_url}?{ext}"
        response = requests.get(url, timeout=5)
        return response.json()

    def get_data_for_date_interval(self, date_from, date_to):
        url = f"{self.base_url}?&date_from={date_from}&date_to={date_to}"
        pagination = self.get_pagination(url)
        collected_data = []
        for page in range(0, pagination):
            params = {
                'date_from': date_from,
                'date_to': date_to,
                'per_page': self.per_page,
                'page': page
            }
            response = self.fetch_page(params)
            collected_data.extend(response.get('items', []))
            
            if len(response.get('items', [])) < self.per_page:
                break  # Нет больше страниц
            

        return collected_data


    def get_data(self):
        response = [self.get_data_for_date_interval(interval["date_from"], interval["date_to"]) for interval in self.hour_interval]

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
