up-local:
	  export DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 # enable buildkit
		docker-compose build
		docker-compose run --rm web python manage.py migrate
		docker-compose up
down-local:
	docker-compose -f docker-compose.yml down -v
