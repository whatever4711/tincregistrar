#!/bin/bash
docker-compose up -d
sleep 5
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose restart web
docker-compose run web /bin/bash -c "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
