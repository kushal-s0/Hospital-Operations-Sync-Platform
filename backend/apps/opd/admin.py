from django.contrib import admin
from .models import OPDQueue, OPDStatistics

@admin.register(OPDQueue)
class OPDQueueAdmin(admin.ModelAdmin):
    list_display = ['token_number', 'patient', 'department', 'status', 'priority', 'check_in_time']
    list_filter = ['status', 'priority', 'department']
    search_fields = ['patient__first_name', 'patient__last_name', 'token_number']

@admin.register(OPDStatistics)
class OPDStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'department', 'total_patients', 'average_wait_time']
    list_filter = ['department']
