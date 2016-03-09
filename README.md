# tincregistrator


Build up Django application
```
d-cp run web django-admin.py startproject composeexample .
d-cp run web python manage.py startapp test
```

Commands:

```[bash]
#!/bin/bash
d-cp down -v
d-cp build
d-cp up -d
sleep 2
d-cp run web python manage.py migrate
d-cp restart web
d-cp run web python manage.py createsuperuser
```

Debugging
```
docker run -it -v $PWD:/usr/src/app  -p 8000:8000 --link tincregistrator_db_1:db --net="tincregistrator_default" tincregistrator_web /bin/bash
```
