#! /bin/sh

sudo docker-compose -f local.yml run --rm django python manage.py makemigrations && sudo docker-compose -f local.yml run --rm django python manage.py migrate
