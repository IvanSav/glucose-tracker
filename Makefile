.PHONY: up test

up:
	docker-compose up -d --build

down:
	docker-compose down

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

test:
	docker-compose exec web python manage.py test

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

format:
	black .
	isort .

lint:
	black --check .
	isort --check .
