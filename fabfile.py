from fab_deploy import *

@define_host('iserwis@lule.pl')
def my_site():
    return dict(
        DB_USER = '',
        DB_PASSWORD = '',
    )

my_site()
