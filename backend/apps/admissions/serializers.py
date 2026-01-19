from rest_framework import serializers
from apps.authentication.models import Admission
from .models import AdmissionRule
from apps.patients.serializers import PatientSerializer
from apps.beds.serializers import BedSerializer


class AdmissionSerializer(serializers.ModelSerializer):
    """Serializer for Admission model."""
    
    patient_name = serializers.SerializerMethodField()
    bed_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Admission
        fields = ['admission_id', 'patient', 'patient_name', 'bed', 'bed_info', 
                  'doctor', 'admission_time', 'discharge_time', 'condition_level', 
                  'status', 'created_at', 'updated_at', 'admin_id']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_bed_info(self, obj):
        if obj.bed:
            return f"Bed {obj.bed.bed_id}"
        return None


class AdmissionRuleSerializer(serializers.ModelSerializer):
    """Serializer for AdmissionRule model."""
    
    class Meta:
        model = AdmissionRule
        fields = '__all__'
