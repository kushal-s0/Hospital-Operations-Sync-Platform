from rest_framework import serializers
from .models import OPDQueue, OPDStatistics
from apps.authentication.models import Visit, Appointment
from apps.patients.serializers import PatientSerializer


class OPDQueueSerializer(serializers.ModelSerializer):
    """Serializer for OPDQueue model."""
    
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OPDQueue
        fields = '__all__'
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None


class OPDStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for OPDStatistics model."""
    
    class Meta:
        model = OPDStatistics
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for Visit model."""
    
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Visit
        fields = ['visit_id', 'patient', 'patient_name', 'hospital', 'department',
                  'visit_datetime', 'day_of_week', 'season', 'time_of_day',
                  'urgency_level', 'nurse_patient_ratio', 'specialist_availability',
                  'time_to_registration_min', 'time_to_triage_min',
                  'time_to_medical_professional_min', 'total_wait_time_min',
                  'patient_outcome', 'patient_satisfaction', 'created_at', 'admin_id']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model."""
    
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient', 'patient_name', 'doctor', 'visit',
                  'appointment_date', 'appointment_time', 'reason_for_visit',
                  'status', 'created_at', 'updated_at', 'admin_id']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
