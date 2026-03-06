import httpx
from app.core.config import settings

class hhClient():
    def __init__(self):
        self.client = httpx.Client(
            base_url=settings.hh_base_url,
            headers=settings.get_hh_headers(),
        )

    def fetch_vacancies(self, params: dict):
        resp = self.client.get("/vacancies", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def fetch_area(self):
        resp = self.client.get("/areas")
        resp.raise_for_status()
        return resp.json()