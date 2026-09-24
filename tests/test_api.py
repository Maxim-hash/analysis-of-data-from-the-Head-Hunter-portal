# tests/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_vacancies_empty(client: AsyncClient):
    response = await client.get("/vacancies/")
    assert response.status_code == 200
    # пока HTML, поэтому просто проверяем статус
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_list_roles(client: AsyncClient):
    response = await client.get("/roles/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)