from rest_framework import serializers
from .models import OPDQueue, OPDStatistics
from apps.patients.serializers import PatientSerializer


class OPDQueueSerializer(serializers.ModelSerializer):
    """Serializer for OPDQueue model."""
    
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OPDQueue
        fields = '__all__'
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"


class OPDStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for OPDStatistics model."""
    
    class Meta:
        model = OPDStatistics
        fields = '__all__'
