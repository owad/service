"""
#1. Download new repo
#2. Unzip it
#3. Link new repo
#4. Create media_files symlink
#5. Create admin symlink
6. Change DEBUG to False
#7. Copy live_settings.py to new repo's directory
8. Reload apache
"""

from datetime import datetime
from fabric.api import run, warn
from fabric.contrib.files import sed

def download():
    run('cd www && wget https://github.com/owad/service/tarball/master')
    run('cd www && tar xvfz master')
    run('cd www && mv owad-service-* iserwis-new')
    run('rm www/master')

def create_symlinks():
    run('cd www/iserwis-new && ln -s ../iserwis_media_files/ media_files')
    run('cd www/iserwis-new/static_media && ln -s /usr/local/lib/python2.6/dist-packages/Django-1.3-py2.6.egg/django/contrib/admin/media/ admin')


def copy_settings():
    run('cp www/iserwis/live_settings.py www/iserwis-new/live_settings.py')


def replace_current_build():
    run('cd www && mv iserwis iserwis-%s' % datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
    run('cd www && mv iserwis-new iserwis')


def amend_settings():
    sed('www/iserwis/settings.py', 'DEBUG = True', 'DEBUG = False')


def reload_apache():
    run('sudo /etc/init.d/apache2 reload')


def deploy():
    warn('Downloading...')
    download()
    warn('Creating symlinks...')
    create_symlinks()
    warn('Copying live settings...')
    copy_settings()
    warn('Replacing current version...')
    replace_current_build()
    warn('Amending settings...')
    amend_settings()
    warn('Reloading apache...')
    reload_apache()
    warn('It\'s done!!!')
