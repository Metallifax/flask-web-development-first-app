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
```shell
# The application instance for the active application
current_app| application context

# An object that the application can use for temporary
# storage during the handling of a request. Reset with each
# request
     g    |  application context

# The request object, which encapsulates the contents of an
# HTTP request sent by the client
request   |  request context

## The user session, a dictionary that the application can use
# to store values that are "remembered" between requests.
session  |  request context
```

**Four basic Request Hooks:**

```shell
# Register a function to run before the first
# request is handled
>>> before_first_request

# Register a function to run before each request
>>> before_request

# Register a function to run after each request,
# If no unhandled exceptions occurred
>>> after_request

# Register a function to run after each request,
# even if unhandled exceptions occurred
>>> teardown_request
```

### Special Responses

**Creating a Response Object:**

```python
from flask import make_response

@app.route('/')
def index():
  response = make_response('<h1>This document carries a cookie!</h1>')
  response.set_cookie('answer', '42')
  return response
```

**Creating a Redirect:**

```python
from flask import redirect

@app.route('/')
def index():
  return redirect('http://www.example.com')
```

**Creating an Abort function:**

```python
from flask import abort

@app.route('/user/<id>')
def get_user(id):
  user = load_user(id)
  if not user:
    abort(404)
  return f'<h1>Hello, {user.name}</h1>
```
