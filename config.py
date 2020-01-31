# config.py

import os



TOP_DIR = os.path.abspath(os.path.dirname(__file__))
#APP_DIR =  TOP_DIR + '/app'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + TOP_DIR + '/bookie.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# (Necessary for flashes (at least))
SECRET_KEY = 'A very special value... do not share it with anyone! Nadie!'

# Flask-WTF
#WTF_CSRF_SECRET_KEY = SECRET_KEY + '(eep)'