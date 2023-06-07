#!/bin/sh

export FLASK_APP=app.py
export FLASK_DEBUG=0

flask run --port=5000
