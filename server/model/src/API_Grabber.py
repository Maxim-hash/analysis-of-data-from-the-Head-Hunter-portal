from datetime import datetime, timedelta
import httpx
import asyncio

class API_Grabber():
    def __init__(self, per_page=100, max_vacancies=2000):
        self.base_url = "https://api.hh.ru/vacancies"
        self.per_page = per_page
        self.max_vacancies = max_vacancies
        generator = DateIntervalGenerator()
        self.two_week_interval = generator.generate_two_week_intervals()

    async def fetch_page(self, client, params):
        response = await client.get(self.base_url, params=params)
        return response.json()

    async def get_data_for_date_interval(self, client, date_from, date_to):
        collected_data = []
        for page in range(0, self.max_vacancies, self.per_page):
            params = {
                'date_from': date_from,
                'date_to': date_to,
                'per_page': self.per_page,
                'page': page // self.per_page
            }
            response = await self.fetch_page(client, params)
            collected_data.extend(response.get('items', []))
            if len(response.get('items', [])) < self.per_page:
                break  # Нет больше страниц

        return collected_data


    async def get_data(self):
        async with httpx.AsyncClient() as client:
            tasks = [self.get_data_for_date_interval(client, interval['date_from'], interval['date_to']) for interval in self.two_week_interval]
            results = await asyncio.gather(*tasks)
            return results
        

class DateIntervalGenerator:
    def __init__(self):
        self.today = datetime.today()
        self.one_year_ago = self.today - timedelta(days=365)

    def generate_two_week_intervals(self):
        intervals = []
        current_start_date = self.one_year_ago
        while current_start_date < self.today:
            current_end_date = current_start_date + timedelta(days=13)  # Добавляем 13 дней, чтобы получить полные две недели
            if current_end_date > self.today:
                current_end_date = self.today
            intervals.append({
                'date_from': current_start_date.strftime('%Y-%m-%d'),
                'date_to': current_end_date.strftime('%Y-%m-%d')
            })
            current_start_date += timedelta(days=14)  # Переходим к следующему интервалу
        return intervals
