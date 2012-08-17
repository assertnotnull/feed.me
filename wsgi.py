import os
import sys
# put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, '/var/local/python/feedme/')
sys.path.insert(0, '/var/local/python/env/infojdemapps/lib/python2.6/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "feedme.settings.active"
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()