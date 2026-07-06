include .env
export 

export PROJECT_ROOT = $(shell pwd)

env-up:
	@docker compose up -d --build analisys-postgres

env-down:
	@docker compose down -v analisys-postgres

app-up:
	@docker compose up -d --build app

app-down:
	@docker compose down app

worker-up:
	@docker compose up -d --build worker

worker-down:
	@docker compose down worker

migrate: 
	docker compose run --rm migrations alembic upgrade head

migrate-down:
	docker compose run --rm migrations alembic downgrade -1

migrate-down-all: 
	docker compose run --rm migrations alembic downgrade base

migrate-create: 
	@if [ -z "$(MSG)" ]; then \
		echo "Ошибка: укажите MSG. Пример: make migrate-create MSG=\"add new field\""; \
		exit 1; \
	fi;
	docker compose run --rm migrations alembic revision --autogenerate -m "$(MSG)"

down: worker-down app-down env-down
	
up: env-up app-up worker-up

