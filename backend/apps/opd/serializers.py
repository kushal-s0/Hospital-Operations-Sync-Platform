from rest_framework import serializers
from .models import OPDQueue, OPDStatistics
from apps.authentication.models import Visit, Appointment, Patient, StaffUser, Department
from apps.patients.serializers import PatientSerializer


class OPDQueueSerializer(serializers.ModelSerializer):
    """Serializer for OPDQueue model."""
    
    patient_name = serializers.SerializerMethodField()
    patient = PatientSerializer(read_only=True)
    doctor_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    
    # Fields for creating new patients
    patient_first_name = serializers.CharField(write_only=True, required=False)
    patient_last_name = serializers.CharField(write_only=True, required=False)
    contact_number = serializers.CharField(write_only=True, required=False)
    
    # Accept doctor and department by ID or name
    doctor_id = serializers.IntegerField(write_only=True, required=False)
    department_id = serializers.IntegerField(write_only=True, required=False)
    doctor_name_input = serializers.CharField(write_only=True, required=False, source='doctor_name_temp')
    department_name_input = serializers.CharField(write_only=True, required=False, source='department_name_temp')
    
    class Meta:
        model = OPDQueue
        fields = '__all__'
        extra_kwargs = {
            'doctor': {'read_only': True},
            'department': {'read_only': True},
        }
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_doctor_name(self, obj):
        if obj.doctor:
            return f"{obj.doctor.first_name} {obj.doctor.last_name}"
        return None
    
    def get_department_name(self, obj):
        if obj.department:
            return obj.department.department_name
        return None
    
    def create(self, validated_data):
        from django.db.models import Max
        from django.utils import timezone
        
        # Extract patient data
        patient_first_name = validated_data.pop('patient_first_name', None)
        patient_last_name = validated_data.pop('patient_last_name', None)
        contact_number = validated_data.pop('contact_number', None)
        
        # Extract doctor and department data
        doctor_id = validated_data.pop('doctor_id', None)
        department_id = validated_data.pop('department_id', None)
        doctor_name_temp = validated_data.pop('doctor_name_temp', None)
        department_name_temp = validated_data.pop('department_name_temp', None)
        
        # Create or get patient if new patient data provided
        if patient_first_name and patient_last_name:
            # Get next patient ID
            max_patient = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
            next_patient_id = (max_patient or 0) + 1
            
            # Create new patient
            patient = Patient.objects.create(
                patient_id=next_patient_id,
                first_name=patient_first_name,
                last_name=patient_last_name,
                contact_number=contact_number,
                registration_date=timezone.now().date()
            )
            validated_data['patient'] = patient
        
        # Handle doctor - try to find by ID first, then by name
        if doctor_id:
            try:
                doctor = StaffUser.objects.get(staff_id=doctor_id, role='Doctor')
                validated_data['doctor'] = doctor
            except StaffUser.DoesNotExist:
                pass
        elif doctor_name_temp:
            # Try to find doctor by name
            doctors = StaffUser.objects.filter(role='Doctor')
            for doc in doctors:
                if doctor_name_temp.lower() in doc.full_name.lower():
                    validated_data['doctor'] = doc
                    break
        
        # Handle department - try to find by ID first, then by name
        if department_id:
            try:
                department = Department.objects.get(department_id=department_id)
                validated_data['department'] = department
            except Department.DoesNotExist:
                pass
        elif department_name_temp:
            # Try to find department by name
            try:
                department = Department.objects.filter(department_name__icontains=department_name_temp).first()
                if department:
                    validated_data['department'] = department
            except Department.DoesNotExist:
                pass
        
        # Auto-generate token number if not provided
        if 'token_number' not in validated_data:
            max_token = OPDQueue.objects.aggregate(Max('token_number'))['token_number__max']
            validated_data['token_number'] = (max_token or 0) + 1
        
        # Set timestamps
        if 'check_in_time' not in validated_data:
            validated_data['check_in_time'] = timezone.now()
        if 'created_at' not in validated_data:
            validated_data['created_at'] = timezone.now()
        
        # Create queue entry
        return super().create(validated_data)


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
