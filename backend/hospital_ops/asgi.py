"""
ASGI config for hospital_ops project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')

application = get_asgi_application()
