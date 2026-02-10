import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advanced_features_and_security.settings")
application = get_wsgi_application()