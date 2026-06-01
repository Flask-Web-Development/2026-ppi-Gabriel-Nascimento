from glob import escape

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def user(username):
    return f'User {escape(username)}'

@app.route('/contrario/<nomecontrario>')
def contrario(nomecontrario):
    return f'Seu nome ao contrario é: {escape(nomecontrario[::-1])}'


        