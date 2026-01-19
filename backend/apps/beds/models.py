from django.db import models
# Import models from authentication to use the MySQL-mapped versions
from apps.authentication.models import Department, Bed

# Re-export for backwards compatibility
__all__ = ['Department', 'Bed']
