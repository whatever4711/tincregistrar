#!/bin/bash
docker-compose up -d
sleep 5
docker exec tincregistrator_web_1 python manage.py makemigrations
docker exec tincregistrator_web_1 python manage.py migrate
docker-compose restart web
docker exec tincregistrator_web_1 /bin/bash -c "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
