from rest_framework import serializers
from apps.authentication.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'full_name', 'gender', 
                  'date_of_birth', 'contact_number', 'address', 'registration_date',
                  'insurance_provider', 'insurance_number', 'email', 'created_at', 
                  'updated_at', 'admin_id']
