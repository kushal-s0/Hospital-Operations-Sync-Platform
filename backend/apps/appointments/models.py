from django.db import models
from apps.authentication.models import Patient, StaffUser as Doctor, Appointment

# Re-export Appointment model for use in this app
__all__ = ['Appointment']
