from rest_framework import serializers
from apps.authentication.models import Appointment, Patient, StaffUser, Department


class AppointmentBookingSerializer(serializers.Serializer):
    """Serializer for booking appointments from landing page"""
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    contact_number = serializers.CharField(max_length=20)
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = serializers.CharField(required=False, allow_blank=True)
    
    # Appointment details
    appointment_date = serializers.DateField()
    appointment_time = serializers.TimeField()
    department_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField(required=False, allow_null=True)
    reason_for_visit = serializers.CharField(max_length=200)
    
    def validate_appointment_date(self, value):
        """Ensure appointment date is not in the past"""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for appointment management"""
    patient_name = serializers.SerializerMethodField()
    patient_contact = serializers.SerializerMethodField()
    patient_email = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'appointment_id', 'patient', 'doctor', 'visit',
            'appointment_date', 'appointment_time', 'reason_for_visit',
            'status', 'created_at', 'updated_at',
            'patient_name', 'patient_contact', 'patient_email',
            'doctor_name', 'department_name'
        ]
        read_only_fields = ['appointment_id', 'created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        try:
            if obj.patient:
                return f"{obj.patient.first_name} {obj.patient.last_name}".strip()
        except Exception:
            pass
        return None
    
    def get_patient_contact(self, obj):
        try:
            return obj.patient.contact_number if obj.patient else None
        except Exception:
            return None
    
    def get_patient_email(self, obj):
        try:
            return obj.patient.email if obj.patient else None
        except Exception:
            return None
    
    def get_doctor_name(self, obj):
        try:
            # Get doctor from StaffUser table using doctor_id
            if hasattr(obj, 'doctor_id') and obj.doctor_id:
                doctor = StaffUser.objects.filter(staff_id=obj.doctor_id).first()
                if doctor:
                    return f"Dr. {doctor.first_name} {doctor.last_name}".strip()
        except Exception as e:
            print(f"Error getting doctor name: {e}")
        return None
    
    def get_department_name(self, obj):
        try:
            # Get department from StaffUser table using doctor_id
            if hasattr(obj, 'doctor_id') and obj.doctor_id:
                doctor = StaffUser.objects.filter(staff_id=obj.doctor_id).first()
                if doctor and doctor.department:
                    return doctor.department.department_name
        except Exception as e:
            print(f"Error getting department name: {e}")
        return None


class AppointmentStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating appointment status"""
    status = serializers.ChoiceField(choices=['Scheduled', 'Approved', 'Completed', 'Cancelled'])
    notes = serializers.CharField(required=False, allow_blank=True)
