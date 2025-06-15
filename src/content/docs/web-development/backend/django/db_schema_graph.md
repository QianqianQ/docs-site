---
title: Database Schema Graph
description: Unit tests commands.
---

How to generate graphs of database schema for Django apps:
```bash
cd app/
# Activate the virtual environment
source <virtualenv_path>/bin/activate

# Install python packages
# For Django 2.2, django-extensions<=3.1.5
# django-extensions>=3.2.1 only supoort Django 3.2 and later
# Check https://github.com/django-extensions/django-extensions/releases
pip install django-extensions==x.x.x

# pydot: Python interface to Graphviz and its DOT language
pip install pydot

# Installing python package graphviz fails, while it is optional, so this step could be skipped
# https://django-extensions.readthedocs.io/en/latest/graph_models.html#selecting-a-library
# pip install pygraphviz
# sudo apt-get install graphviz  # appear to be no use
```

```python
# Add 'django-extensions' to 'INSTALLED_APPS' in app/app/settings.py
INSTALLED_APPS = {
    ...
    'django_extensions',
    ...
}
```

```bash
# Generate the schema picture
# See example usage: https://django-extensions.readthedocs.io/en/latest/graph_models.html#example-usage
./manage.py graph_models -a -g -o schema.png
# with explicit selection of pydot
./manage.py graph_models --pydot -a -g -o schema.png
# Specify app(s)
./manage.py graph_models <app_name> -o schema.png
# Example
./manage.py graph_models vbgf -o vbgf_schema.png
```