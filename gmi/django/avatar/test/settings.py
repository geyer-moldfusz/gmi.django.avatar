INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'gmi.django.avatar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

SECRET_KEY = 'xxx'

STATIC_URL = '/static/'
