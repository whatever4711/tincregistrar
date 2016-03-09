#!/bin/bash
docker-compose up -d
sleep 2
docker-compose run web python manage.py migrate
docker-compose restart web
docker-compose run web python manage.py createsuperuser
