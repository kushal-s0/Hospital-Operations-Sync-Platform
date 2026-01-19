from rest_framework import serializers
from apps.authentication.models import InventoryItem, InventoryUsage
from .models import InventoryCategory, InventoryTransaction


class InventoryCategorySerializer(serializers.ModelSerializer):
    """Serializer for InventoryCategory model."""
    
    class Meta:
        model = InventoryCategory
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for InventoryItem model."""
    
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['item_id', 'item_name', 'category', 'quantity_available', 
                  'reorder_level', 'supplier', 'is_low_stock', 'created_at', 
                  'updated_at', 'admin_id']


class InventoryTransactionSerializer(serializers.ModelSerializer):
    """Serializer for InventoryTransaction model."""
    
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = '__all__'


class InventoryUsageSerializer(serializers.ModelSerializer):
    """Serializer for InventoryUsage model."""
    
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = InventoryUsage
        fields = ['usage_id', 'item', 'item_name', 'patient', 'patient_name',
                  'quantity_used', 'usage_date', 'department', 'created_at', 'admin_id']
    
    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return None
