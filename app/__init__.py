# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import cli, jinja, models, views

#
# Register modules
#

from .mods.bookmark import mod as modBookmark
app.register_blueprint(modBookmark, url_prefix='/bookmarks')