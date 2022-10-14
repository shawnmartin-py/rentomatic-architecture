all: down build up

test:
	./manage.py test -- --integration -s

build:
	./manage.py compose build web

up:
	./manage.py compose up -d

down:
	./manage.py compose down

db:
	./manage.py init-postgres