#!/bin/sh

export FLASK_APP=api.py
export FLASK_DEBUG=1

flask run --port=5000
