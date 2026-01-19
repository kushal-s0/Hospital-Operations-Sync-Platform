from rest_framework import serializers
from .models import Department, Bed


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    
    bed_count = serializers.SerializerMethodField()
    available_beds = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def get_bed_count(self, obj):
        return obj.beds.count()
    
    def get_available_beds(self, obj):
        return obj.beds.filter(status='available').count()


class BedSerializer(serializers.ModelSerializer):
    """Serializer for Bed model."""
    
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Bed
        fields = '__all__'
