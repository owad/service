# config file for environment-specific settings
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ DB_NAME }}',
        'USER': '{{ DB_USER }}',
        'PASSWORD': '{{ DB_PASSWORD }}',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB"
        },
    }
}
