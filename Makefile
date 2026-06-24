include .env
export 

export PROJECT_ROOT = $(shell pwd)

env-up:
	@docker compose up -d analisys-postgres

env-down:
	@docker compose down analisys-postgres

app-up:
	@docker compose up -d app

app-down:
	@docker compose down app

worker-up:
	@docker compose up -d worker

worker-down:
	@docker compose down worker

migrate: ## Применить все миграции (upgrade head)
	docker compose run --rm migrations alembic upgrade head

migrate-up: migrate   # alias

migrate-down: ## Откатить последнюю миграцию
	docker compose run --rm migrations alembic downgrade -1

migrate-down-all: ## Откатить все миграции
	docker compose run --rm migrations alembic downgrade base

migrate-create: ## Создать новую миграцию
	@if [ -z "$(MSG)" ]; then \
		echo "Ошибка: укажите MSG. Пример: make migrate-create MSG=\"add new field\""; \
		exit 1; \
	fi;
	docker compose run --rm migrations alembic revision --autogenerate -m "$(MSG)"

down: worker-down app-down env-down
	

up: env-up app-up worker-up

