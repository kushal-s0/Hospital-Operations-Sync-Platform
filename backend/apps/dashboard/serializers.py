from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary data."""
    
    total_beds = serializers.IntegerField()
    available_beds = serializers.IntegerField()
    occupied_beds = serializers.IntegerField()
    occupancy_rate = serializers.FloatField()
    total_opd_patients_today = serializers.IntegerField()
    waiting_patients = serializers.IntegerField()
    current_admissions = serializers.IntegerField()
    low_stock_items = serializers.IntegerField()
