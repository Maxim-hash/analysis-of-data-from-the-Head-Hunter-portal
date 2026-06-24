FROM python:3.12-slim-bookworm

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем Alembic конфигурацию и код
COPY alembic.ini ./
COPY app/ ./app/
COPY worker/ ./worker/

EXPOSE 8000
