.SILENT:

build:
	docker compose -f docker-compose.yml build
	docker compose -f docker-compose.yml --compatibility up -d

connect-db:
	docker compose exec postgres psql --username=hello_flask --dbname=hello_flask_dev