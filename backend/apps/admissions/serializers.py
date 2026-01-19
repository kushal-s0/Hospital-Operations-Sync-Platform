from rest_framework import serializers
from .models import Admission, AdmissionRule
from apps.patients.serializers import PatientSerializer
from apps.beds.serializers import BedSerializer


class AdmissionSerializer(serializers.ModelSerializer):
    """Serializer for Admission model."""
    
    patient_name = serializers.SerializerMethodField()
    bed_number = serializers.CharField(source='bed.bed_number', read_only=True)
    
    class Meta:
        model = Admission
        fields = '__all__'
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"


class AdmissionRuleSerializer(serializers.ModelSerializer):
    """Serializer for AdmissionRule model."""
    
    class Meta:
        model = AdmissionRule
        fields = '__all__'
