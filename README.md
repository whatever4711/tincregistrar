# tincregistrar


## Build up Django application
```
docker-compose run web django-admin.py startproject composeexample .
docker-compose run web python manage.py startapp test
```

### Commands:

```[bash]
#!/bin/bash
docker-compose up -d
sleep 5
docker exec tincregistrar_web_1 python manage.py makemigrations
docker exec tincregistrar_web_1 python manage.py migrate
docker-compose restart web
docker exec tincregistrar_web_1 /bin/bash -c "echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
```

### Debugging
```
# For Postgresql
docker run -it -v $PWD:/usr/src/app  -p 8000:8000 --link tincregistrar_db_1:db --net="tincregistrar_default" tincregistrar_web /bin/bash
# For Sqlite
docker run -it -v $PWD:/usr/src/app -v tincregistrar_sqlitedb:/usr/src/app/tinc/data -p 8000:8000 --net="tincregistrar_default" tincregistrar_web /bin/bash
```

Usage within curl:
- Upload your tinc configuration with ```curl -H "Authorization: $AUTH_TOKEN" -X POST -T $YOURTINCCONFIG serverIP:8000/regService/config```
- Get configuration of other clients with ```curl -H "Authorization: $AUTH_TOKEN" serverIP:8000/regService/config```
- Delete your tinc configuration with ```curl -H "Authorization: $AUTH_TOKEN" -X DELETE serverIP:8000/regService/config```

## Client
### Just install tinc with:
```
sudo modprobe tun

sudo apt-get update && sudo apt-get install -y tinc
echo tun | sudo tee -a /etc/modules

```
### Edit ./tincsetup
Enter your `CONFIG_SERVER` and / or the other parameters at the top.

### Start using tinc
Now you can use `chmod a+x ./tincsetup && ./tincsetup` to configure your network.



TODOs

- Adjustable private network
- Support for several network names
