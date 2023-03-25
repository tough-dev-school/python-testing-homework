up-local:
	export DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 # enable buildkit
	docker-compose build
	docker-compose run --rm web python manage.py migrate
	docker-compose up

up-d-local:
	export DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 # enable buildkit
	docker-compose build
	docker-compose run --rm web python manage.py migrate
	docker-compose up -d

down-local:
	docker-compose -f docker-compose.yml down -v

logs:
	docker-compose logs -f

format:
	@echo "> Formatting + style checking..."
	isort tests
	black -S tests
	flake8 tests
	@echo "> Formatting + style checking... finished.\n"
