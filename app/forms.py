# app/forms.py

from wtforms import Field, Form, StringField
from wtforms.validators import DataRequired, Length, URL
from wtforms.widgets import TextInput

from .models import Tag



class TagListField(Field):
    """
    Custom field for (comma-separated) tag lists.
    Described here: http://wtforms.readthedocs.io/en/latest/fields.html#custom-fields
    """
    
    widget = TextInput()
  
    def _value(self):
        if self.data:
            nameList = Tag.TagsToNames(self.data)
            return ', '.join(nameList)
        else:
            return ''
    
    def process_formdata(self, namesStr):
        if namesStr:
            namesList = [ tn.strip() for tn in namesStr[0].split(',') ]
            namesList = list( set(namesList) )  # remove duplicates
            self.data = Tag.NamesToTags(namesList)  # also creates any new tags
        else:
            self.data = []
