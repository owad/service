# config file for environment-specific settings
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iserwis',
        'USER': 'iserwis',
        'PASSWORD': 'dupa.8',
        'HOST': 'lule.pl',
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB"
        },
    }
}
