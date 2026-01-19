from django.contrib import admin
from .models import Department, Bed

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor', 'created_at']
    search_fields = ['name']

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['bed_number', 'department', 'bed_type', 'status', 'room_number']
    list_filter = ['status', 'bed_type', 'department']
    search_fields = ['bed_number', 'room_number']
