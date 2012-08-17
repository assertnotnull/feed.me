from settings import *
import ConfigParser

config = ConfigParser.RawConfigParser()
path = os.path.abspath(__file__+'/../../../mysql.cfg')
config.read(path)

DEBUG = False

ADMINS = (
    ('Patrice Gauthier', 'patgauth@gmail.com')
    )

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'feedme.db',                      # Or path to database file if using sqlite3.
        'USER': config.get('mysql','user'),                      # Not used with sqlite3.
        'PASSWORD': config.get('mysql','password'),                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
