setup: ## setup project
	poetry install
	poetry shell
	psql postgres -U postgres -f scripts/create_dev_database.sql
	poetry python manage.py migrate
	poetry python manage.py createsuperuser

run: ## run server
	poetry run python manage.py runserver

lint: ## run linter
	poetry run isort .
	poetry run flake8 .

mypy: ## run mypy
	poetry run mypy server tests/**/*.py

test: ## run tests
	poetry run pytest .

help: ## this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# .PHONY: setup run lint mypy test help
.DEFAULT_GOAL := help
