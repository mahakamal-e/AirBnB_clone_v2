#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Get all state data"""
    states = storage.all("State")
    return render_template("9-states.html",
                           states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def cities_by_states(id):
    """Get all state data"""
    states = storage.all("State")
    state_id = "State." + id

    if state_id in states.keys():
        return render_template("9-states.html",
                               state=states[state_id],
                               id=id)

    return render_template("9-states.html", not_found="not found")


@app.teardown_appcontext
def terminate(exc):
    """Close SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
