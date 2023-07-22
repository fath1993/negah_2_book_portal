import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'negah_2_book_portal.settings')

application = get_asgi_application()
