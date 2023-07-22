from negah_2_book_portal.settings import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', 'webops.ir', 'www.webops.ir', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'charset': 'utf8mb4'},
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/webopsir/public_html/static'
MEDIA_ROOT = '/home/webopsir/public_html/media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]
