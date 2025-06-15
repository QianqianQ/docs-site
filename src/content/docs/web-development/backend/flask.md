---
title: Flask
description: Flask.
---

- WSGI web application framework
- getting started quick and easy, with the ability to scale up to complex applications

```bash
mkdir myproject
cd myproject
python3 -m venv .venv
. .venv/bin/activate

pip install Flask

flask --app <app_name> run --port 5000
# if the file is named app.py or wsgi.py, you don’t have to use --app
# --app hello:app  # Uses the app Flask instance in hello
# --debug  # enable debug mode
# --host=0.0.0.0 tells your operating system to listen on all public IPs. It allows you to access the development server from other devices on the same network. When running a Flask application inside a Docker container, you might use --host=0.0.0.0 to expose the Flask application to the host machine or other devices.
```

## Deployment

### WSGI servers
#### Gunicorn
```bash
pip install gunicorn

gunicorn -w 4 'hello:app'  # equivalent to 'from hello import app'
gunicorn -w 4 'hello:create_app()'  # from hello import create_app; create_app()
```

#### mod_wsgi
a WSGI server integrated with the Apache httpd server
```bash
pip install mod_wsgi
```

#### uWSGI
- A fast, compiled server suite with extensive configuration and capabilities beyond a basic server.
- It does not support Windows (but does run on WSL).
- It requires a compiler to install in some cases.
- multiple ways to install it
```bash
# does not provide SSL support, which can be provided with a reverse proxy instead
pip install pyuwsgi

# If you have a compiler available, you can install the uwsgi package instead. Or install the pyuwsgi package from sdist instead of wheel. Either method will include SSL support.
pip install uwsgi
pip install --no-binary pyuwsgi pyuwsgi

# --master option specifies the standard worker manager
uwsgi --http 127.0.0.1:8000 --master -p 4 -w wsgi:app
```

- uWSGI should not be run as root because it would cause your application code to run as root, which is not secure. However, this means it will not be possible to bind to port 80 or 443.
- a reverse proxy such as nginx or Apache httpd should be used in front of uWSGI.
- uWSGI has optimized integration with Nginx uWSGI and Apache mod_proxy_uwsgi, and possibly other servers, instead of using a standard HTTP proxy.

#### ASGI
```python
from asgiref.wsgi import WsgiToAsgi
from flask import Flask

app = Flask(__name__)

asgi_app = WsgiToAsgi(app)
```
```bash
hypercorn module:asgi_app
```

### HTTP servers
WSGI servers have HTTP servers built-in. However, a dedicated HTTP server may be safer, more efficient, or more capable. Putting an HTTP server in front of the WSGI server is called a “reverse proxy.” The proxy will intercept and forward all external requests to the local WSGI server.

HTTP servers should set `X-Forwarded-` headers to pass on the real values to the application. The application can then be told to trust and use those values by wrapping it with the `X-Forwarded-For Proxy Fix` middleware provided by Werkzeug. See https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/

#### nginx
#### Apache httpd

## HTML Escaping

When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be escaped to protect from injection attacks. HTML templates rendered with Jinja will do this automatically.
```python
from markupsafe import escape

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
```

If a user managed to submit the name `<script>alert("bad")</script>`, escaping causes it to be rendered as text, rather than running the script in the user’s browser.

`<name>` in the route captures a value from the URL and passes it to the view function.

## Variable Rules
`<variable_name>` or `<converter:variable_name>`. converter types: string (without a slash), int, float, path (accept slash), uuid
```python
@app.route('/user/<username>')
@app.route('/post/<int:post_id>')
@app.route('/path/<path:subpath>')
```

## Unique URLs / Redirection Behavior
- `@app.route('/projects/')` -> similar to a folder in a file system. `/projects` -> `/projects/`.
- `@app.route('/projects')` -> similar to a pathname of a file. `/projects/` -> `404 “Not Found” error`.
-  This helps keep URLs unique for these resources, which helps search engines avoid indexing the same page twice.

## URL Building
`url_for`

## HTTP Methods
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

# You can also separate views for different methods into different functions. Flask provides a shortcut for decorating such routes with get(), post(), etc. for each common HTTP method
@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()
```

## Static files
Create a folder called `static` in your package or next to your module and it will be available at `/static` on the application.

To generate URLs for static files, use the special 'static' endpoint name
```python
url_for('static', filename='style.css')
# static/style.css
```

## Rendering Templates
Flask will look for templates in the `templates` folder
```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)
```
Jinja2:
- have access to the config, request, session and g objects as well as the url_for() and get_flashed_messages() functions.
- Template Inheritance. possible to keep certain elements on each page (like header, navigation and footer).
- Automatic escaping is enabled, so if person contains HTML it will be escaped automatically.
- mark safe variable or HTML as safe by using the Markup class or by using the `|safe` filter in the template.
For Jinja2, see https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates

## Accessing Request Data
### Test request
```python
from flask import request

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'

# or passing a whole WSGI environment to the request_context() method:
with app.request_context(environ):
    assert request.method == 'POST'
```

### The Request Object
```python
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

# To access parameters submitted in the URL (?key=value) you can use the args attribute:
searchword = request.args.get('key', '')
```

## File uploads
Set `enctype="multipart/form-data"` attribute on your HTML form, otherwise the browser will not transmit your files at all. Uploaded files are stored in memory or at a temporary location on the filesystem.
```python
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
    ...

# If you want to use the filename of the client to store the file on the server, pass it through the secure_filename() function that Werkzeug provides for you:
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")
    ...
```

## Cookies
The `cookies` attribute of request objects is a dictionary with all the cookies the client transmits. If you want to use sessions, do not use the cookies directly but instead use the `Sessions` in Flask that add some security on top of cookies for you.
```python
from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
```

## Deferred Request Callbacks
```python
from flask import request, after_this_request

@app.before_request
def detect_user_language():
    language = request.cookies.get('user_lang')

    if language is None:
        language = guess_language_from_request()

        # when the response exists, set a cookie with the language
        @after_this_request
        def remember_language(response):
            response.set_cookie('user_lang', language)
            return response

    g.language = language
```

## Redirects and Errors
```python
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
```

## Responses
If a response object of the correct type is returned it’s directly returned from the view.

If it’s a string, a response object is created with that data and the default parameters.  (with the string as response body, a `200 OK` status code and a `text/html` mimetype)

If it’s an iterator or generator returning strings or bytes, it is treated as a streaming response.

If it’s a dict or list, a response object is created using `jsonify()`.

If a tuple is returned the items in the tuple can provide extra information. Such tuples have to be in the form (response, status), (response, headers), or (response, status, headers). The status value will override the status code and headers can be a list or dictionary of additional header values.

If none of that works, Flask will assume the return value is a valid WSGI application and convert that into a response object.

https://flask.palletsprojects.com/en/stable/quickstart/#about-responses

## APIs with JSON
If you return a dict or list from a view, it will be converted to a JSON response.
```python
# all the data in the dict or list must be JSON serializable.

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]
```

## Sessions
In addition to the request object there is also a second object called session which allows you to store information specific to a user from one request to the next. This is implemented on top of cookies for you and signs the cookies cryptographically. What this means is that the user could look at the contents of your cookie but not modify it, unless they know the secret key used for signing.
```python
from flask import session

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
```

## Message Flashing
To flash a message use the `flash()` method, to get hold of the messages you can use `get_flashed_messages()` which is also available in the templates. See
https://flask.palletsprojects.com/en/stable/patterns/flashing/

## Logging
```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```

## Hooking in WSGI Middleware
```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
```
Wrapping app.wsgi_app instead of app means that app still points at your Flask application, not at the middleware, so you can continue to use and configure app directly.