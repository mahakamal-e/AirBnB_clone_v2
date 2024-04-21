#!/usr/bin/python3
"""Start flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states():
    """display a HTML page"""
    states = storage.all('State')
    amenities = storage.all('Amenity')
    places = storage.all('Place')
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    """Close SqlAlqemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
