# Update DATABASES configurations
{'django_db': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'django_db',
    'USER': db_user,
    'PASSWORD': db_pass,
    'HOST': 'db',
    'PORT': '5432',
    'TEST': {
        'NAME': get_test_db_name() + "django"
    }
    }
}
