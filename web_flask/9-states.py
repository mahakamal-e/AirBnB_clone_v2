#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states')
def states():
    """Displays HTML containes all state data"""
    states = storage.all("State")
    return render_template("9-states.html",
                           states=states)


@app.route('/states/<id>')
def cities_by_states(id):
    """Displays HTML containes state data related to City"""
    states = storage.all("State")
    _id = "State." + id
    if _id in states.keys():
        return render_template("9-states.html", state=states[_id],
                               id=id)

    return render_template("9-states.html", not_found="not found")


@app.teardown_appcontext
def terminate(exc):
    """Close SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
