from rest_framework import serializers
from .models import OPDQueue, OPDStatistics
from apps.authentication.models import Visit, Appointment, Patient, StaffUser, Department, Doctor
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
            'patient': {'read_only': True},
            'token_number': {'required': False},
            'check_in_time': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False},
            'consultation_start_time': {'required': False},
            'consultation_end_time': {'required': False},
            'estimated_wait_time': {'required': False},
            'admin_id': {'required': False},
            'id': {'read_only': True},
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
        doctor_assigned = False
        if doctor_id:
            try:
                doctor = StaffUser.objects.get(staff_id=doctor_id, role='Doctor')
                validated_data['doctor'] = doctor
                doctor_assigned = True
            except StaffUser.DoesNotExist:
                pass
        
        if not doctor_assigned and doctor_name_temp:
            # Try to find doctor by name
            doctors = StaffUser.objects.filter(role='Doctor', is_active=True)
            for doc in doctors:
                if doctor_name_temp.lower() in doc.full_name.lower():
                    validated_data['doctor'] = doc
                    doctor_assigned = True
                    break
        
        # If still no doctor, assign first available doctor
        if not doctor_assigned:
            first_doctor = StaffUser.objects.filter(role='Doctor', is_active=True).first()
            if first_doctor:
                validated_data['doctor'] = first_doctor
            else:
                raise serializers.ValidationError({'doctor': 'No active doctors found in the system'})
        
        # Handle department - try to find by ID first, then by name
        department_assigned = False
        if department_id:
            try:
                department = Department.objects.get(department_id=department_id)
                validated_data['department'] = department
                department_assigned = True
            except Department.DoesNotExist:
                pass
        
        if not department_assigned and department_name_temp:
            # Try to find department by name
            department = Department.objects.filter(department_name__icontains=department_name_temp).first()
            if department:
                validated_data['department'] = department
                department_assigned = True
        
        # If still no department, assign first available department
        if not department_assigned:
            first_dept = Department.objects.first()
            if first_dept:
                validated_data['department'] = first_dept
            else:
                raise serializers.ValidationError({'department': 'No departments found in the system'})
        
        # Auto-generate token number if not provided
        if 'token_number' not in validated_data:
            max_token = OPDQueue.objects.aggregate(Max('token_number'))['token_number__max']
            validated_data['token_number'] = (max_token or 0) + 1
        
        # Set timestamps
        if 'check_in_time' not in validated_data or not validated_data['check_in_time']:
            validated_data['check_in_time'] = timezone.now()
        if 'created_at' not in validated_data or not validated_data['created_at']:
            validated_data['created_at'] = timezone.now()
        
        # Set updated_at
        validated_data['updated_at'] = timezone.now()
        
        # Create queue entry
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError({'error': f'Failed to create queue entry: {str(e)}'})


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
    doctor_name = serializers.SerializerMethodField()
    contact_number = serializers.SerializerMethodField()
    doctor_id = serializers.IntegerField(write_only=True, required=False)
    doctor_name_input = serializers.CharField(write_only=True, required=False)
    
    # Fields for creating new patients
    patient_first_name = serializers.CharField(write_only=True, required=False)
    patient_last_name = serializers.CharField(write_only=True, required=False)
    contact_number_input = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient', 'patient_name', 'doctor', 'doctor_name', 
                  'doctor_id', 'doctor_name_input', 'patient_first_name', 'patient_last_name',
                  'contact_number', 'contact_number_input', 'visit', 'appointment_date', 
                  'appointment_time', 'time_slot', 'age', 'reason_for_visit',
                  'status', 'created_at', 'updated_at', 'admin_id']
        extra_kwargs = {
            'doctor': {'read_only': True},
            'patient': {'read_only': True},
            'appointment_id': {'read_only': True},
        }
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
    
    def get_doctor_name(self, obj):
        if obj.doctor and obj.doctor.staff:
            return f"{obj.doctor.staff.first_name} {obj.doctor.staff.last_name}"
        return None
    
    def get_contact_number(self, obj):
        if obj.patient:
            return obj.patient.contact_number
        return None
    
    def create(self, validated_data):
        """Handle doctor and patient assignment during creation."""
        doctor_id = validated_data.pop('doctor_id', None)
        doctor_name_input = validated_data.pop('doctor_name_input', None)
        
        # Handle patient creation
        patient_first_name = validated_data.pop('patient_first_name', None)
        patient_last_name = validated_data.pop('patient_last_name', None)
        contact_number = validated_data.pop('contact_number_input', None)
        
        # Create or get patient
        if patient_first_name or patient_last_name:
            from django.utils import timezone
            from django.db.models import Max
            
            # Get the next patient_id (in case auto_increment isn't working)
            max_patient_id = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
            next_patient_id = (max_patient_id or 0) + 1
            
            patient = Patient(
                patient_id=next_patient_id,
                first_name=patient_first_name,
                last_name=patient_last_name,
                contact_number=contact_number,
                registration_date=timezone.now().date()
            )
            patient.save()
            validated_data['patient'] = patient
        
        # Handle doctor - try to find by staff_id (which is the doctor_id in the UI)
        doctor_assigned = False
        if doctor_id:
            try:
                # doctor_id from frontend is actually staff_id
                doctor = Doctor.objects.get(staff_id=doctor_id)
                validated_data['doctor'] = doctor
                doctor_assigned = True
            except Doctor.DoesNotExist:
                pass
        
        if not doctor_assigned and doctor_name_input:
            # Try to find doctor by name in staff users
            staff_users = StaffUser.objects.filter(role='Doctor')
            for staff in staff_users:
                if doctor_name_input.lower() in staff.full_name.lower():
                    try:
                        doctor = Doctor.objects.get(staff=staff)
                        validated_data['doctor'] = doctor
                        doctor_assigned = True
                        break
                    except Doctor.DoesNotExist:
                        pass
        
        return super().create(validated_data)
