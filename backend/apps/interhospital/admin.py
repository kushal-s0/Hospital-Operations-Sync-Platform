from django.contrib import admin
from .models import Hospital, CapacitySnapshot

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'city', 'is_active', 'created_at']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'code']

@admin.register(CapacitySnapshot)
class CapacitySnapshotAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'total_beds', 'available_beds', 'icu_beds_available', 'timestamp']
    list_filter = ['hospital', 'timestamp']
