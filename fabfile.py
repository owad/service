from fab_deploy import *

def my_site():
    env.hosts = ['owad@localhost']
    env.conf = dict(
        DB_USER = '',
        DB_PASSWORD = '',
        OS = 'ubuntu'
    )
    update_env()

my_site()