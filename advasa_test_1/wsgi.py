import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advasa_test_1.settings')

application = get_wsgi_application()

