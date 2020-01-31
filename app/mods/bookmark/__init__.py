# app/mods/bookmark/__init__.py

from flask import Blueprint

mod = Blueprint('bookmark', __name__, template_folder='templates', static_folder='static')

from . import jinja, models, views