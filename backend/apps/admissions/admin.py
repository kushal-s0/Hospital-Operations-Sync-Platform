from django.contrib import admin
from .models import Admission, AdmissionRule

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'bed', 'admission_type', 'status', 'admission_date']
    list_filter = ['status', 'admission_type', 'admission_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']

@admin.register(AdmissionRule)
class AdmissionRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'recommended_department', 'recommended_bed_type', 'priority', 'is_active']
    list_filter = ['is_active', 'recommended_department']
