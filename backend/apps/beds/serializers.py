from rest_framework import serializers
from apps.authentication.models import Department, Bed


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    
    class Meta:
        model = Department
        fields = ['department_id', 'hospital', 'department_name', 'total_beds', 
                  'available_beds', 'emergency_beds', 'created_at', 'updated_at', 'admin_id']


class BedSerializer(serializers.ModelSerializer):
    """Serializer for Bed model."""
    
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    class Meta:
        model = Bed
        fields = ['bed_id', 'hospital', 'department', 'department_name', 'bed_type', 
                  'status', 'created_at', 'updated_at', 'admin_id']
