#!/usr/bin/python3
"""
Starts a flask web application
"""
from flask import Flask
import re


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    new_text = re.sub('_', ' ', text)
    return f'C {new_text}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
