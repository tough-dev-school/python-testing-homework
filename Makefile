# test: ## run tests
# 	poetry run coverage run --source=task_manager -m pytest tests

test: ## run tests
	poetry run pytest .

lint: ## run linter
	poetry run flake8 .

run: ## run local server
	poetry run python manage.py runserver

help: ## this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# .PHONY: install test lint selfcheck check build package-install cc-coverage help init setup
.DEFAULT_GOAL := help
