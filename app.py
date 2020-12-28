from flask import Flask, request, render_template
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  return f"<h1>Hello World!</h1><p>Your browser is {user_agent}</p>"

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)

if __name__ == '__main__':
  manager.run()
