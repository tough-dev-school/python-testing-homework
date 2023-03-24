.EXPORT_ALL_VARIABLES:

DOTENV_BASE_FILE ?= config/.env
COMPOSE_FILE ?= docker-compose.yml
POETRY ?= $(HOME)/.local/bin/poetry
APP = server
TESTS ?= tests/**/*.py

-include $(DOTENV_BASE_FILE)

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	$(POETRY) self update

.PHONY: docker-up-local
docker-up-local:
	docker-compose -f $(COMPOSE_FILE) up --remove-orphans -d
	docker-compose -f $(COMPOSE_FILE) ps

.PHONY: docker-down-local
docker-down-local:
	docker-compose -f $(COMPOSE_FILE) down

.PHONY: docker-down-volumes-local
docker-down-volumes-local:
	docker-compose -f ${COMPOSE_FILE} down --volumes

.PHONY: docker-restart
docker-restart: docker-down-local docker-up-local

.PHONY: docker-logs
docker-logs:
	docker-compose -f ${COMPOSE_FILE} logs --follow

.PHONY: lint
lint:  ## Lint and static-check
	@echo 'Checking started...'
	$(POETRY) run isort --check-only --diff $(TESTS)
	$(POETRY) run flake8 --diff $(TESTS)
	$(POETRY) run mypy $(APP) $(TESTS) --show-error-codes
	$(POETRY) run yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .
	$(POETRY) run dotenv-linter $(DOTENV_BASE_FILE)
	@echo 'Linter and style checking finished! \(^_^)/'

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	$(POETRY) run isort $(TESTS)

.PHONY: fmt-flake
fmt-flake:  ## To get started flake8 recursively
	$(POETRY) run flake8 $(TESTS)

.PHONY: fmt
fmt: fmt-isort fmt-flake

.PHONY: test-slow
test-slow: ## Find slow two tests
	$(POETRY) run pytest --durations=2 --no-cov --disable-warnings

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	$(POETRY) run pytest --disable-warnings --cov-report=term --cov-report=html

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf .cache .pytest_cache .mypy_cache .coverage coverage.xml htmlcov
	@echo 'Cache folders deleted! \(^_^)/'
