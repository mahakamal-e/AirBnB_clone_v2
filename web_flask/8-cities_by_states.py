#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """
    Displays HTML containes all state data
    """
    states = storage.all("State")
    return render_template("8-cities_by_states.html",
                           states=states)


@app.teardown_appcontext
def teardown(exc):
    """Method close SqlAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
