---
title: App Setup
description: How to add an app in a Django project.
---

- [Add an app](#add-an-app)
- [Add an API](#add-an-api)
- [Add templates and static files](#add-templates-and-static-files)

## Add an app
* Create app `python manage.py startapp <app_name>`. This creates a new folder named app_name with the basic structure needed for the app

* Register in `app/app/settings.py`
  - `INSTALLED_APPS`: Add the app `<app_name>`
  - `TEMPLATES`:
    + Add `os.path.join(BASE_DIR, <app_name>, 'templates')`. With `APP_DIRS` set to `True`and put html files under `BASE_DIR/<app_name>/templates/<app_name>/`, the template loader will look in the apps templates directory and find the templates, and then it is not necessary to add templates path to `TEMPLATES`
  - `DATABASE_APPS_MAPPING`:
    + Add `<app_name>: '<app_name>_db'`
  - `DATABASES`:
    + Add new database configuration

* Register in `routers.py`
  - Update `allow_migrate()` function. Only allow `<app_name>_db` to be migrated to `<app_name>` app. Details about `allow_migrate()`: https://docs.djangoproject.com/en/5.1/topics/db/multi-db/#allow_migrate

```python
# settings.py
INSTALLED_APPS = {
  <app_name>,
}
TEMPLATES = {
    os.path.join(BASE_DIR, <app_name>, 'templates'),  # optional
    'APP_DIRS': True,
    ...
}
DATABASE_APPS_MAPPING = {
    <app_name>: '<app_name>_db'
}

DATABASES = {
    ...
}

# routers.py. Only allow <app_name>_db to be migrated to <app_name> app
# update allow_migrate()
```

## Add an API
```python
# Define a model in <app_name>/models.py

# Create a serializer in <app_name>/serializers.py. Serializers transform the model instances into JSON (or other formats)

# Define function-based views/class-based views/DRF’s viewsets in <app_name>/api.py

# Configure route for the API in one of <app_name>/urls.py

python manage.py makemigrations
python manage.py migrate
```

## Add templates and static files
* Create HTML file
  - Create html files `BASE_DIR/<app_name>/templates/<app_name>/`
  - Create a view in `<app_name>/views.py`
  - Define a url in `<app_name>/urls.py`
  - Register URLConf in `<app_name>/urls.py` to `app/app/urls.py`

* Create JavaScript file
  - Create JS files under `<app_name>/static/<app_name>/js/`

* Register staticfiles directories:
  - In addition to using `static/` directory inside `<app_name>/` directory, add any required directories to `STATICFILES_DIRS` in `app/app/settings.py`
