# tincregistrator


Build up Django application
```
docker-compose run web django-admin.py startproject composeexample .
docker-compose run web python manage.py startapp test
```

Commands:

```[bash]
#!/bin/bash
docker-compose up -d
sleep 5
docker exec tincregistrator_web_1 python manage.py makemigrations
docker exec tincregistrator_web_1 python manage.py migrate
docker-compose restart web
docker exec tincregistrator_web_1 /bin/bash -c "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
```

Debugging
```
docker run -it -v $PWD:/usr/src/app  -p 8000:8000 --link tincregistrator_db_1:db --net="tincregistrator_default" tincregistrator_web /bin/bash
```

Usage within curl:
- Upload your tinc configuration with ```curl -X POST -T $YOURTINCCONFIG serverIP:8000/regService/config```
- Get configuration of other clients with ```curl serverIP:8000/regService/config```
- Delete your tinc configuration with ```curl -X DELETE serverIP:8000/regService/config```

TODOs

- Adjustable private network
- Support for several network names
