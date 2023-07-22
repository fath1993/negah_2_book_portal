import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'negah_2_book_portal.c_settings.prod')

application = get_wsgi_application()
