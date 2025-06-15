#!/bin/bash
# This script performs migrations on multiple databases, populates dimensioning_db and creates a  superuser.
read -p "This will create new databases and delete the existing ones. The existing data will be lost. Do you want to continue? [Y/n] " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then

    echo "Starting migration of DB"

    echo ">> Recreating django DB"

sudo su - postgres <<EOF
dropdb django
createdb -O django -E 'UTF8' django
psql -c '\l'
exit
EOF

    echo ">> Deleting old migrations"
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -name "*.pyc" -not -path "./excluded*" -exec rm -rf {} \;

    find . -name "default_db" -delete

    echo ">> Migrate django_db"
    python manage.py makemigrations django
    python manage.py migrate --database=django_db django

    echo ">> Apply migrations"
    python manage.py makemigrations
    python manage.py migrate

    sleep 3s

    echo ">> Create superuser"
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

    echo ">> Load data to DBs"
    python manage.py loaddata --database=django_db django/app/database/data.json

    echo ">> Done"
fi
