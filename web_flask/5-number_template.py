#!/usr/bin/python3
""" Starts a Flask web application. """
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ Displays Hello HBNB """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Displays HBNB """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_txt(text):
    """ Displays “C ” followed by the value of the text variable. """
    textWithoutUnderscore = text.replace('_', ' ')
    return "C " + textWithoutUnderscore


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_txt(text):
    """ Displays “Python ” followed by the value of the text variable."""
    textWithoutUnderscore = text.replace('_', ' ')
    return "Python " + textWithoutUnderscore


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Displays number if is integer. """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays an HTML page with the number."""
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
