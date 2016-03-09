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
