import os
import sys

path = '/var/www/demo.serwis.lechkom.pl'
if path not in sys.path:
    sys.path.append(path) 

os.environ['DJANGO_SETTING_MODULE'] = 'www.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

