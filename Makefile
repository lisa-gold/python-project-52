MANAGE := poetry run python manage.py

.PHONY: test
test:
	@poetry run pytest

start:
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus

.PHONY: lint
lint:
	@poetry run flake8 task_manager
