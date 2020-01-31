# app/jinja.py

from app import app
from app.models import Tag



#
# Filters
#

def formatStamp(td):
    if td:
        fmt = td.strftime( '%Y-%m-%d %H:%M:%S' )
    else:
        fmt = ''

    return fmt

app.jinja_env.filters['formatStamp'] = formatStamp


def tagListToStr(tagList):
    return ', '.join( Tag.TagsToNames(tagList) )

app.jinja_env.filters['tagListToStr'] = tagListToStr