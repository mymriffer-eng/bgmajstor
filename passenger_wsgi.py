import os
import sys

# Добави пътя до проекта
sys.path.insert(0, os.path.dirname(__file__))

# Настрой Django settings module за production
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'

# Импортирай WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
