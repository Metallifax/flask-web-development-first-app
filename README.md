# Flask Web Development

Follows the book "Flask Web Development" by Miguel Grinberg

* Project starts on Chapter 2 *

<img src="book-cover.jpg">

## Useful Commands

**Show url map:**

```shell
>>> from app import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
 <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

## Useful Knowledge

### Context Globals

| Variable Name | Context | Description |
| ------------- | ------- | ----------- |
| current_app | Application Context | The application instance for the active application. |
| g | Application Context | An object that the application can use for temporary storage during the handling of a request. This variable is reset with each request. |
| request | Request Context | The request object, which encapsulates the contents of a HTTP request sent by the client. |
| session | Request Context | The user session, a dictionary that the application can use to store values that are "remembered" between requests. |

Four basic Request Hooks:

| Hook | Description |
| ------------- | ------- |
| before_first_request | Register a function to run before the first request is handled.|
| before_request | Register a function to run before each request. |
| after_request | Register a function to run after each request, if no unhandled exceptions occurred.|
| teardown_request | Register a function to run after each request, even in unhandled exception occurs. |

### Special Responses

Creating a Response Object:

```python
from flask import make_response

@app.route('/')
def index():
  response = make_response('<h1>This document carries a cookie!</h1>')
  response.set_cookie('answer', '42')
  return response
```

*reating a Redirect:

```python
from flask import redirect

@app.route('/')
def index():
  return redirect('http://www.example.com')
```

Creating an Abort function:

```python
from flask import abort

@app.route('/user/<id>')
def get_user(id):
  user = load_user(id)
  if not user:
    abort(404)
  return f'<h1>Hello, {user.name}</h1>
```

### Command Line Options with Flask-Script

first install

```shell
> pipenv install flask-script
```

Update the application script

```python
from flask.ext.script import Manager

manager = Manager(app)

# ...

if __name__ == '__main__':
  manager.run()
```

Now you can view the command line utility usage message

```shell
> python app.py
usage: app.py [-?] {shell,runserver} ...

positional arguments:
  {shell,runserver}
    shell            Runs a Python shell inside Flask application context.
    runserver        Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help         show this help message and exit

> python app.py runserver --help
usage: app.py runserver [-?] [-h HOST] [-p PORT] [--threaded] 
[--processes PROCESSES] [--passthrough-errors] [-d] [-D] [-r] 
[-R] [--ssl-crt SSL_CRT] [--ssl-key SSL_KEY]

Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
  -h HOST, --host HOST
  -p PORT, --port PORT
  --threaded
  --processes PROCESSES
  --passthrough-errors
  -d, --debug           enable the Werkzeug debugger 
                        (DO NOT use in production code)
  -D, --no-debug        disable the Werkzeug debugger
  -r, --reload          monitor Python files for changes 
                        (not 100% safe for production use)
  -R, --no-reload       do not monitor Python files for changes
  --ssl-crt SSL_CRT     Path to ssl certificate
  --ssl-key SSL_KEY     Path to ssl key

> python app.py runserver
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a 
            production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [28/Dec/2020 17:31:55] "GET / HTTP/1.1" 200 -

# Changing the host server
> python app.py runserver --host 0.0.0.0
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in 
            a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

### Rendering Templates

```python
from flask import Flask, render_template

# ...

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)
```

### Examples of Variables in Templates

```html
<p>A value from a dictionary: {{ mydict['key'] }}</p>
<p>A value from a list: {{ mylist[3] }}</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}</p>
<p>A value from an object's method: {{ myobj.somemethod() }}</p>
```

### Jinja2 Variable filters

| Filter Name | Description |
| ----------- | ----------- |
| safe | Renders the value without applying escaping|
| capitalize | Converts the first character of the value to uppercase and the rest to lowercase|
| lower | Converts the value to lowercase characters |
| upper | Converts the value to uppercase characters |
| title | Capitalizes each word in the value |
| trim | Removes the leading and trailing whitespaces from the value |
| striptags | Removes any HTML tags from the value before rendering |

**Important Note:**
*Never use safe filter on values that aren't trusted, such as input fields*

**Complete list of jinja filters here:**
*https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters*

### Template Control Structures

Conditional statements

```html
{% if user %}
  Hello, {{ user }}!
{% else %}
  Hello, stranger!
{% endif %}
```

List of elements

```html
<ul>
  {% for comment in comments %}
    <li>{{ comment }}</li>
  {% endfor %}
</ul>
```

Jinja2 macros

```html
{% macro render_comment(comment) %}
  <li>{{ comment }}</li>
{% endmacro %}

<ul>
  {% for comment in comments %}
    {{ render_comment(comment) }}
  {% endfor %}
</ul>
```

To make macros more reusable, they can be stored in standalone files that are then *imported* from all the templates that need them:

```html
{% import 'macros.html' as macros %}
<ul>
  {% for comment in comments %}
    {{ macros.render_comment(comment) }}
  {% endfor %}
</ul>
```

Portions of template code that need to be repeated in several places can be stored in a seperate file and included from all the templates to avoid repetition:

```html
{% include 'common.html' %}
```

A more powerful way would be to reuse through template inheritance, which is similar to class inheritance in Python code.

First we create the base file that will be inherited.

```html
<!-- base.html -->
<html>
  <head>
    {% block head %}
      <title>{% block title %}{% endblock%} - My Application</title>
    {% endblock %}
  </head>
  <body>
    {% block body %}
    {% endblock %}
  </body>
</html>
```

And we extend it in another template

```html
<!-- index.html -->
{% extends 'base.html' %}

{% block title %}Index{% endblock %}

{% block head %}
  {{ super() }}
  <style>
  </style>
{% endblock %}

{% block body %}
  <h1>Hello, World!</h1>
{% endblock %}
```

### Twitter Bootstrap Integration

The simple approach to integrating BS4 is to install the flask extension

```shell
> pipenv install flask-bootstrap
```

Import the extension in app.py

```python
from flask.ext.bootstrap import Bootstrap

# ...

bootstrap = Bootstrap(app)
```
