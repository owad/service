import os
import sys

import site
site.addsitedir('/home/owad/company/lib/python2.6/site-packages')
 
path = '/srv/www/demo'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/demo')
    sys.path.insert(0, '/srv/www/demo/www')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

