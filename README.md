### Hexlet tests and linter status:
[![Actions Status](https://github.com/lisa-gold/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lisa-gold/python-project-52/actions)
[![Python CI](https://github.com/lisa-gold/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/lisa-gold/python-project-52/actions/workflows/pyci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/96cb7230003f8dfa8d17/maintainability)](https://codeclimate.com/github/lisa-gold/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/96cb7230003f8dfa8d17/test_coverage)](https://codeclimate.com/github/lisa-gold/python-project-52/test_coverage)

### Description
This is a web application that helps to manage users' tasks. Here you can add, update and delete tasks, statuses of tasks, and labels that can be added to tasks.

### Link 
https://python-project-52-kfee.onrender.com/

### This project was build using these tools:
| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [poetry](https://python-poetry.org/)                                        | "Python dependency management and packaging made easy"  |
| [pip](https://pypi.org/project/pip/)                                        | "Package installer for Python"                          |
| [Django](https://www.djangoproject.com/)                                    | "Django makes it easier to build better web apps more quickly and with less code" |
| [flake8](https://flake8.pycqa.org/)                                         | "Your tool for style guide enforcement" |
| [gunicorn](https://docs.gunicorn.org/en/stable/)                            | "Python WSGI HTTP Server for UNIX" |
| [uvicorn](https://www.uvicorn.org/)                                         | "Uvicorn is an ASGI web server implementation for Python" |
|[python-dotenv](https://pypi.org/project/python-dotenv/)                     | "Python-dotenv reads key-value pairs from a .env file and can set them as environment variables" |
|[render](https://docs.render.com/)                                           | "Render is a unified cloud to build and run all your apps and websites" |
|[bootstrap](https://getbootstrap.com/)                                       | "Feature-packed frontend toolkit" |
|[psycopg](https://www.psycopg.org/docs/index.html)                           | "Database adapter" |
|[dj-database-url](https://pypi.org/project/dj-database-url/)                 | "This simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application" |
|[WhiteNoise](https://whitenoise.readthedocs.io/en/stable/index.html)         | "Radically simplified static file serving for Python web apps" |
|[django-extensions](https://django-extensions.readthedocs.io/en/latest/)     | "Collection of custom extensions for the Django Framework" |
|[pytest-django](https://pytest-django.readthedocs.io/en/latest/)             | "Plugin for pytest that provides a set of useful tools for testing Django applications and projects" |
|[django-filter](https://django-filter.readthedocs.io/en/stable/)             | "It allows users to filter down a queryset based on a model’s fields, displaying the form to let them do this" |
|[rollbar](https://rollbar.com/lizik.gold/)                                   | "Discover, predict, and resolve errors in real-time" |

### Example of .env
SECRET_KEY = 'secret'
DEBUG = 'True'
DATABASE_URL = 'postgresql:...'
ROLLBAR_TOKEN = 'token'
