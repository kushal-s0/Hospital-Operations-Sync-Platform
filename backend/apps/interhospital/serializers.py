from rest_framework import serializers
from .models import Hospital, CapacitySnapshot


class HospitalSerializer(serializers.ModelSerializer):
    """Serializer for Hospital model."""
    
    class Meta:
        model = Hospital
        fields = '__all__'


class CapacitySnapshotSerializer(serializers.ModelSerializer):
    """Serializer for CapacitySnapshot model."""
    
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    hospital_code = serializers.CharField(source='hospital.code', read_only=True)
    occupancy_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = CapacitySnapshot
        fields = '__all__'
    
    def get_occupancy_rate(self, obj):
        if obj.total_beds > 0:
            occupied = obj.total_beds - obj.available_beds
            return round((occupied / obj.total_beds * 100), 2)
        return 0


class CityDashboardSerializer(serializers.Serializer):
    """Serializer for anonymized city-level data."""
    
    hospital_code = serializers.CharField()
    available_beds = serializers.IntegerField()
    icu_beds_available = serializers.IntegerField()
    occupancy_rate = serializers.FloatField()
    last_updated = serializers.DateTimeField()
