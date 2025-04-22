"""
WSGI config for timetracker project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetracker.settings')

application = get_wsgi_application()