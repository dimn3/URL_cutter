from os import getenv

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=getenv('SECRET_KEY', default='SECRET_KEY'),
    JSON_AS_ASCII=False,
))

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from . import api_views, error_handlers, views
