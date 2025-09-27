from .settings import *

# PythonAnywhere specific settings
DEBUG = False
ALLOWED_HOSTS = ['ronald03.pythonanywhere.com']

# Database configuration for PythonAnywhere MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ronald03$default',
        'USER': 'ronald03',
        'PASSWORD': 'your-database-password',
        'HOST': 'ronald03.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}