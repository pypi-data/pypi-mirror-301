# backend/inc_counter/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    return app

