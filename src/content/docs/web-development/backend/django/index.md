---
title: Django
description: Comprehensive Django reference covering setup, development, testing, security, and deployment.
sidebar:
  label: Complete Guide
  order: 0  # Make it appear first
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
---

**Tech Stack**
- Python3
- Django web framework <br>
  **NB** Python & Django version compatibility. https://docs.djangoproject.com/en/5.0/faq/install/#faq-python-version-support
- Apache with mod_wsgi module activated for production deployment
- PostgreSQL with psycopg or psycopg2 package
- Ansible for automating app deployment

### Python

```bash
# Install python
# Fetches the latest version of the package list
sudo apt-get update  # or sudo apt update
sudo apt-get install python3.6

# Python3.8
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8

# Verify python version
python3 --version
# To see if pip is installed
command -v pip
command -v pip3

# Optional: symlink support is installed too on Ubuntu Linux version 20.04 LTS and above
sudo apt install python-is-python3

# Possible dependencies
# python3-pip: a Python package manager hosted by Python Software Foundation, broader and can install Python packages of a particular version
# virtualenv: this tool isololates Python packages from other Python projects or system Python packages, thus prevents dependency problems.
# python3-dev, libpq-dev: solve problem with psycopg2
# libldap2-dev libsasl2-dev libssl-dev: solve problem with python-ldap
sudo apt-get install -y python3-pip virtualenv python3-dev libpq-dev python3-distutils libldap2-dev libsasl2-dev libssl-dev

# VENV
sudo apt-get install python3-venv    # If needed
python3 -m venv .venv
source .venv/bin/activate
# Alternative: virtualenv
mkdir ${HOME}/virtualenvs
virtualenv -p python3 <virtualenv_path>
source <virtualenv_path>/bin/activate
# NB. It is a good idea to keep all your virtual environments in one place, for example in .virtualenvs/ in your home directory.

# Deactivate the venv
deactivate

# To confirm the virtual environment is activated, check the location of Python interpreter
which python
pip3 -V

# symlink support is installed too on Ubuntu Linux version 20.04 LTS and above
sudo apt install python-is-python3

# Install Django
pip install django
pip install --upgrade (-U) Django
python -m django --version

# Find django source files location
python -c "import django; print(django.__path__)"
```

### Django

#### Add App
```bash
# Start django project
django-admin startproject mysite

# Create an empty development database
python manage.py migrate

# Add django app
python manage.py startapp polls

# Add view function: views.py

# Map the view to a URL: urls.py

# Config the global URLconf in the porject to include polls.urls:
# mysite/urls.py: include()

# Interactive mode
python manage.py shell

# Create requirements.txt
pip freeze > requirements.txt
```

#### Database Setup
```bash
# Config mysite/settings.py DATABASES

# In mysite/settings.py INSTALLED_APPS: Add new app

# Create models: models.py
# NB: It is important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objectsâ€™ representations are used throughout Djangoâ€™s automatically-generated admin.

# Generate scripts in the migrations folder that migrate the database from its current state to the new state
migrate python manage.py makemigrations polls

# Take migration names and return their SQL
python manage.py sqlmigrate polls 0001

# Check issues without making mrgration or touching db
python manage.py check

# Take all the migrations not applied and run on db. apply the scripts to the actual database
python manage.py migrate

# (Write data into your database using the Django administrative utility loaddata command)
```

#### DB Operation

> **F function**: reducing the number of queries some operations require
>> We can also use update() to increment the field value on multiple objects - which could be very much faster than pulling them all into Python from the database, looping over them, incrementing the field value of each one, and saving each one back to the database: Reporter.objects.update(stories_filed=F("stories_filed") + 1)

#### Admin Site
```bash
# Create admin user
python manage.py createsuperuser --username=<username> --email=<email>

# Admin site urls. This path is included by default when creating the app: in urls.py
path("admin/", admin.site.urls)

# Set STATIC_ROOT for rendering admin site css: in settings.py
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# Translation is turn on by default: in settings.py
LANGUAGE_CODE = 'en-us'

# Register models to admin and make it visible and editable: in /app/admin.py
admin.site.register(Question)

# Custom admin form: in /app/admin.py
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]

admin.site.register(Question, QuestionAdmin)

# Custom admin template

# Add modified base_site.html to mysite/templates/admin/base_site.html
# (There are also some settings like django.contrib.admin.AdminSite.site_header could be modified to modify template)
```

#### Views

##### Add views function -> Add url mapping
Decouple apps from the project-level URLconf using an include

> URL Example: `path("<int:question_id>/", views.detail, name="detail")`
>>Using angle brackets â€œcapturesâ€ part of the URL and sends it as a keyword argument to the view function.<br>
The question_id part of the string defines the name that will be used to identify the matched pattern, and the int part is a converter that determines what patterns should match this part of the URL path. The colon (:) separates the converter and pattern name.

##### Generic Views System
```python
# django.views.generic

# class-based view e.g., ListView
model = Question
template_name = "polls/index.html"
context_object_name = "last_question_list"

def get_queryset(self):
    return Question.objects.order_by("pub_date")[:5]
```

#### Templates

>The Django templating engine then takes care of making the substitutions when rendering the page, and provides automatic escaping to prevent XSS attacks (that is, if you tried using HTML in a data value, you would see the HTML rendered only as plain text).

```python
# Add templates folder under app folder
# DjangoTemplates looks for a â€œtemplatesâ€ subdirectory in each of the INSTALLED_APPS. settings.py: TEMPALTES: APP_DIRS = True

# Referred as polls/index.html
polls/template/polls/index.html

# Render templates
# In view function, render index.html with context
template = loader.get_template("polls/index.html")
context = {"last_question_list": last_question_list}
return HttpResponse(template.render(context, request))
# Or shortcut
return render(request, "polls/index.html", context)

# URL in template
# using the {% url %} template tag in template
# with 'name' arg in path function
# In template
# <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

# Namespacing URL names
# Add namespaces to URLconf to let Django knows which app view to create for a url when using the {% url %} template tag
# In the polls/urls.py: Add an app_name to set the application namespace:
app_name = "polls"

# In template
# <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

##### Template inheritance
Base template
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>{% block title %}{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}"/>
</head>
<body>
<div class="navbar">
    <a href="{% url 'polls:home' %}" class="navbar-brand">Home</a>
</div>

<div class="body-content">
    {% block content %}
    {% endblock %}
    <hr/>
    <footer>
        <p>&copy; 2018</p>
    </footer>
</div>
</body>
</html>
```

Child tempalte
```html
{% extends "polls/layout.html" %}
{% block title %}Home{% endblock title %}
{% block content %}<p>Home page for the Visual Studio Code Django tutorial.</p>{% endblock content %}
```

**it's possible to generate HTML directly in code, developers avoid such a practice because it opens the app to cross-site scripting (XSS) attacks. A much better practice is to keep HTML out of your code entirely by using templates, so that your code is concerned only with data values and not with rendering.**

#### Forms
```html
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    <fieldset>
        <legend><h1>{{ question.question_text }}</h1></legend>
        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
        {% for choice in question.choice_set.all %}
            <input type="radio" name="choice" id="choice{{forloop.counter}}" value="{{choice.id}}">
            <label for="choice{{forloop.counter}}">{{choice.choice_text}}</label><br>
        {% endfor %}
    </fieldset>
    <input type="submit" value="Vote"></input>
</form>
```

- Use csrf_token to handle Cross Site Request Forgeries
- request.POST is dict-like
- request.POST values are always strings

##### Creating forms from models
1. Create forms.py under app
2. Create subclass of forms.ModelForm

#### Run development server
```bash
# Run server on port ${PORT}, IP address 127.0.0.1
# If ${PORT} is omitted, the default port will be 8000
python manage.py runserver ${PORT}
# (You may consider to use a Firefox private window or Chrome incognito window to prevent local addresses in browsing history)
```

#### Automated Test
- defined In app/tests.py
- subcalss of TestCase
- def test_ methods
- a separate TestClass for each model or view
- a separate test method for each set of conditions you want to test
- test method names that describe their function
- Selenium to test HTML

```bash
python manage.py test app

# Run specific testcase
python manage.py test vbgf.unit_test.test_vbgf_common_calculations.CommonCalculationsTestCase.test_ebm_calc
```

```python
# views test
django.test.Client
response = client.get(reverse("polls:index"))
response.content
response.context["latest_question_list"]
```

#### Code coverage
A good way to spot untested parts of your application is to check code coverage.
This also helps identify fragile or even dead code.<br>
See `Coverage.py`

#### Static files
- `django.contrib.staticfiles`: Collects static files from each of your applications (and any other places you specify) into a single location that can easily be served in production.

- Djangoâ€™s STATICFILES_FINDERS setting contains a list of finders that know how to discover static files from various sources.

>Django will choose the first static file it finds whose name matches, and if you had a static file with the same name in a different application, Django would be unable to distinguish between them. So namespacing them by putting those static files inside another directory named for the application itself.

Example: polls/static/polls/style.css
```html
{% load static %}
<link rel="stylesheet" href="{% static 'polls/style.css'%}">
```

- The {% static %} template tag generates the absolute URL of static files.
- You should always use relative paths to link your static files between each other, because then you can change STATIC_URL (used by the static template tag to generate its URLs) without having to modify a bunch of paths in your static files as well.

##### Serve Static Files in Production
```python
DEBUG=False
ALLOWED_HOSTS = ...

# For static assets not tie to apps
STATICFILES_DIRS = ...
```
Deployment: Same server, Dedicated server, CDN

#### Internationalization
```python
# In views.py
from django.utils.translation import gettext

message = gettext("Welcome to our site!")

# Pluralization
page = ngettext(
    'there is %(count)d object',
    'there are %(count)d objects',
count) % {
    'count': count,
}
```

In template
```html
{% load i18n %}

<title>{% trans "This is the title." %}</title>
<title>{% trans myvar %}</title>

{% comment %}
If your translations require strings with variables {{ value }} (placeholders), use {% blocktrans %}
{% endcomment %}
```

#### Django packages
https://djangopackages.org/

Generally 3-party need to be added to INSTALLED_APPS, some need to add URLconf.

#### Add Django Debug Toolbar
python -m pip install django-debug-toolbar

#### VSCode debuuger
- VSCode debuuger launch profile
    - F5 -> select/add workspace -> add python interpreter
    - Update launch.json
    - Start debugging: F5
    - Close debugger: Shift + F5
- debugger also could be used with page templates

### Docs
```bash
# convert mediawiki to sphinx
docker run --rm --volume "$(pwd):/data" pandoc/core -f mediawiki -t rst -s --list-tables --css=style.css  test.wiki -o test.rst
```

### Security

```python
# API
# webapps/webapps/settings.py

# REST framework configuration
REST_FRAMEWORK = {
    # Allow access to any authenticated user,
    # and deny access to any unauthenticated user.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
```


### Reusability
A Django application is a Python package that is specifically intended for use in a Django project. An application may use common Django conventions, such as having models, tests, urls, and views submodules.

>Application labels (that is, the final part of the dotted path to application packages) must be unique in INSTALLED_APPS. Avoid using the same label as any of the Django contrib packages, for example auth, admin, or messages.


#### Packaging app
1. Install prerequisites: `build` or `setuptools` and `pip`
```bash
pip install --upgrade build

pip install --upgrade setuptools[core]
```

2. Create package dir `mkdir ${package}`

    >When choosing a name for your package, check PyPI to avoid naming conflicts with existing packages. We recommend using a django- prefix for package names, to identify your package as specific to Django, and a corresponding django_ prefix for your module name. For example, the django-ratelimit package contains the django_ratelimit module.

3. Create models, tests, urls, and views submodules

4. Edit `app/apps.py` so that name refers to the new module name and add label to give a short name for the app
    ```python
    class PollsConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "django_polls"
        label = "polls"
    ```

5. Create `app/README.rst`

6. Create `app/LICENSE` file. code released publicly without a license is useless. Django and many Django-compatible apps are distributed under the BSD license

7. Create `pyproject.toml`, (and/or `setup.cfg` and `setup.py`) files which detail how to build and install the app

    - `pyproject.toml`: containing a build-system section. This section declares what are your build system dependencies, and which library will be used to actually do the packaging.
    - In addition to specifying a build system, you also will need to add some package information such as metadata, contents, dependencies, etc. This can be done in the same pyproject.toml file, or in a separated one: `setup.cfg` or `setup.py`.

8. Create `MANIFEST.in` file to include addtional files

9. (Optional, Recommended) Create an empty directory `django-polls/docs` for future documentation

10. Build the package by running `python setup.py sdist`. This creates a directory called `dist` and builds your new package `*.tar.gz`.

#### Using package
1. use `pip` to install the package
```
python -m pip install --user `package/dist/*-0.1.tar.gz`
```

2. Update `mysite/settings.py` to point to the new module name
```python
INSTALLED_APPS = [
    "django_polls.apps.PollsConfig",
    ...,
]
```

3. Update mysite/urls.py to point to the new module name
```python
urlpatterns = [
    path("polls/", include("django_polls.urls")),
    ...,
]
```

>**Installing as a user library**: Per-user installs have a lot of advantages over installing the package system-wide, such as being usable on systems where you donâ€™t have administrator access as well as preventing the package from affecting system services and other users of the machine. But disadvantage: Modifying the user libraries can affect other Python software on your system; wonâ€™t be able to run multiple versions of this package

>Best solution is to **use venv**. maintain multiple isolated Python environments, each with its own copy of the libraries and package namespace.

##### Publish app
- Email the package
- Upload the package on your website
- Post the package on a public repository, such as PyPI
