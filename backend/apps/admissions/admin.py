from django.contrib import admin
from apps.authentication.models import Admission
from .models import AdmissionRule

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['admission_id', 'patient', 'bed', 'condition_level', 'status', 'admission_time']
    list_filter = ['status', 'condition_level']
    search_fields = ['patient__first_name', 'patient__last_name']

@admin.register(AdmissionRule)
class AdmissionRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'recommended_department', 'recommended_bed_type', 'priority', 'is_active']
    list_filter = ['is_active', 'recommended_department']
