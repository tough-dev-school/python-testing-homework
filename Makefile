.EXPORT_ALL_VARIABLES:

COMPOSE_FILE ?= docker-compose.yml
COMPOSE_OVERRIDE_FILE ?= docker-compose.override.yml

DOTENV_BASE_FILE ?= config/.env.template
DOTENV_CUSTOM_FILE ?= config/.env

POETRY = $(HOME)/.local/bin/poetry
APP = server
TESTS = tests/**/*.py

-include $(DOTENV_BASE_FILE)
-include $(DOTENV_CUSTOM_FILE)

# === Poetry ===

.PHONY: update-poetry
update-poetry:  ## Updating Poetry to the latest stable version
	$(POETRY) self update

# === Docker ===

.PHONY: docker-config
docker-config:
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_OVERRIDE_FILE) config

.PHONY: docker-up-local
docker-up-local:
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_OVERRIDE_FILE) up --remove-orphans -d
	docker-compose ps

.PHONY: docker-stop
docker-stop:
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_OVERRIDE_FILE) stop
	docker-compose ps

.PHONY: docker-start
docker-start:
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_OVERRIDE_FILE) start
	docker-compose ps

.PHONY: docker-down-local
docker-down-local:
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_OVERRIDE_FILE) down

.PHONY: docker-down-volumes-local
docker-down-volumes-local:
	docker-compose -f ${COMPOSE_FILE} -f $(COMPOSE_OVERRIDE_FILE) down --volumes

.PHONY: docker-restart
docker-restart: docker-down-local docker-up-local

.PHONY: docker-logs
docker-logs:
	docker-compose -f ${COMPOSE_FILE} -f $(COMPOSE_OVERRIDE_FILE) logs --follow

# === Django ===

.PHONY: shell
shell:  ## Start a Django shell (Interactive Console)
	python manage.py shell

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: server
server:
	python manage.py runserver

# === Linters and formating ===

.PHONY: lint
lint:  ## Lint and static-check
	@echo 'Checking started...'
	isort --check-only --diff $(TESTS)
	flake8 .
	mypy $(APP) $(TESTS) --show-error-codes
	yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .
	dotenv-linter $(DOTENV_BASE_FILE)
	@echo 'Linter and style checking finished! \(^_^)/'

.PHONY: fmt-isort
fmt-isort:  ## To apply isort recursively
	isort $(TESTS)

.PHONY: fmt-flake
fmt-flake:  ## To get started flake8 recursively
	flake8 .

.PHONY: fmt
fmt: fmt-isort fmt-flake

# === Tests ===

.PHONY: find-tests-slow
find-tests-slow: ## Find slow two tests
	pytest --verbose --randomly-seed=default --durations=2 --no-cov --disable-warnings

.PHONY: tests-slow
tests-slow: ## Start tests with 'slow' mark
	pytest --verbose --randomly-seed=default -m "slow" --no-cov --disable-warnings

.PHONY: tests-not-slow
tests-not-slow: ## Start quick tests (without 'slow' mark)
	pytest --verbose --randomly-seed=default -m "not slow" --no-cov --disable-warnings

.PHONY: tests-login
tests-login: ## Start tests with 'login' mark
	pytest --verbose --randomly-seed=default -m "login" --no-cov --disable-warnings

.PHONY: tests-registration
tests-registration: ## Start tests with 'registration' mark
	pytest --verbose --randomly-seed=default -m "registration" --no-cov --disable-warnings

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	pytest --verbose --randomly-seed=default --disable-warnings --cov-report=term --cov-report=html

# === Cache ===

.PHONY: clean
clean:  ## Clean up the cache folders
	@rm -rf .cache .pytest_cache .mypy_cache .coverage coverage.xml htmlcov
	@echo 'Cache folders deleted! \(^_^)/'
