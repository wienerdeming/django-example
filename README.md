# Django example Service

### Tech
Requirements:
 * [Python] +3.5 - Python object oriented programming language
 * [PostgreSQL] +10 - Open source object-relational database system

We use:

* [Django] - is a high-level Python Web framework
* [Django REST framework] - Django REST framework is a powerful and flexible toolkit for building Web APIs

## Installation

### Project

```sh
$ mkdir myproject && cd myproject
$ git clone https://github.com/wienerdeming/django-example.git .
$ virtualenv -p /usr/bin/python3 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```

### Postgres
```
$ su postgres
$ psql
postgres=# CREATE DATABASE mydb;
```

### Run test
```sh
$ python manage.py test
```

### Run
```sh
$ python manage.py runserver
```

### Documentation
Api http://localhost:8000/docs/ also you can find docs in [this](http://api.wienerdeming.com/) link


[Python]: <https://www.python.org/>
[Django]: <https://www.djangoproject.com/>
[Django REST framework]: <http://www.django-rest-framework.org/>
[Celery]: <http://www.celeryproject.org/>
[Postgresql]: <https://www.postgresql.org/>
[Postgis]: <https://www.postgresql.org/>