#!/bin/bash

echo ">> Deleting old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./cn_udr*" -delete
find . -name "*.pyc" -not -path "./excluded*" -exec rm -rf {} \;

find . -name "default_db" -delete

echo ">> Migrate django_db"
python manage.py makemigrations django
python manage.py migrate --database=django_db django



echo ">> Apply migrations"
# python manage.py makemigrations
python manage.py migrate

sleep 3s

echo ">> Create superuser"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

echo ">> Load data to DBs"
python manage.py loaddata --database=django_db djano/database/data.json

echo ">> Done"
