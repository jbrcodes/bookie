# app/mods/bookmark/forms.py

from wtforms import Field, Form, StringField
from wtforms.validators import DataRequired, Length, URL
#from wtforms.widgets import TextInput

from ...forms import TagListField



class BookmarkForm(Form):
    title = StringField('Title', [Length(max=255), DataRequired()])
    url = StringField('URL', [URL(), DataRequired()])
    note = StringField('Note', [Length(max=255)])
    tags = TagListField('Tags')