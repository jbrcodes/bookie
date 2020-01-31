# app/mods/bookmark/jinja.py

from app import app
from .models import Bookmark



#
# Filters
#

app.jinja_env.globals['findAllTags'] = Bookmark.FindAllTags