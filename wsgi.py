import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/owad/venvs/lechkom/lib/python2.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/owad/Projects')
sys.path.append('/home/owad/Projects/lechkom')

os.environ['DJANGO_SETTINGS_MODULE'] = 'lechkom.settings'

activate_env=os.path.expanduser("/home/owad/venvs/lechkom/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
