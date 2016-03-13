#!/bin/bash
docker-compose up -d
sleep 5
docker exec tincregistrator_web_1 python manage.py makemigrations
docker exec tincregistrator_web_1 python manage.py migrate
docker-compose restart web
docker exec tincregistrator_web_1 /bin/bash -c "python manage.py createsuperuser --username admin --email admin@example.com"
