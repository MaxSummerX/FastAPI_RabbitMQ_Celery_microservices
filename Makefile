DC = docker compose
APP_SERVICE = app


.PHONY: app # Запуск контейнеров
app:
	$(DC) up -d


.PHONY: down # Остановка контейнеров
down:
	$(DC) down


.PHONY: migrate # Миграции баз данных
migrate:
	$(DC) exec $(APP_SERVICE) alembic upgrade head


.PHONY: app-logs # Логи приложения
app-logs:
	$(DC) logs -f $(APP_SERVICE)


.PHONY: worker-logs # Логи worker
worker-logs:
	$(DC) logs -f worker

.PHONY: beat-logs # Логи beat
beat-logs:
	$(DC) logs -f beat
