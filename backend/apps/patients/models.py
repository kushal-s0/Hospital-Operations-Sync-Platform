from django.db import models
# Import the Patient model from authentication to use the MySQL-mapped version
from apps.authentication.models import Patient

# Re-export Patient for backwards compatibility
__all__ = ['Patient']
