MANAGE := poetry run python manage.py

install:
	pip install -r requirements.txt

test:
	@$(MANAGE) test

start:
	@$(MANAGE) migrate
	python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

migrate:
	@$(MANAGE) migrate

shell:
	@$(MANAGE) shell_plus

lint:
	@poetry run flake8 task_manager

test-coverage:
	poetry run coverage xml
