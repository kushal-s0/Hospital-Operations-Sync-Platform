from django.contrib import admin
from apps.authentication.models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'first_name', 'last_name', 'contact_number', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'contact_number', 'email']
