from django.contrib import admin
from apps.authentication.models import Department, Bed

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_id', 'department_name', 'hospital', 'total_beds', 'available_beds']
    search_fields = ['department_name']

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['bed_id', 'department', 'bed_type', 'status', 'hospital']
    list_filter = ['status', 'bed_type', 'department']
    search_fields = ['bed_id']
