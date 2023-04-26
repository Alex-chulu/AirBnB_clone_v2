#!/usr/bin/python3
"""
This module provides a simple example of a Flask application with routes
to display different messages.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" at the root route.
    """
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display "HBNB" at the "/hbnb" route.
    """
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_message(text):
    """
    Display "C " followed by the value of the text variable (replace underscore _ symbols with a space)
    at the "/c/<text>" route.

    Args:
        text (str): A string to be displayed after "C ".

    Returns:
        str: A message containing "C " followed by the value of the text variable.
    """
    # Replace underscores in text with spaces
    message = 'C ' + text.replace('_', ' ')

    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
