from rest_framework import serializers
from apps.authentication.models import InventoryItem, InventoryUsage
from .models import InventoryCategory, InventoryTransaction
from django.db import connection


class InventoryCategorySerializer(serializers.ModelSerializer):
    """Serializer for InventoryCategory model."""
    
    class Meta:
        model = InventoryCategory
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for InventoryItem model."""
    
    is_low_stock = serializers.BooleanField(read_only=True)
    item_id = serializers.IntegerField(required=False)
    
    def create(self, validated_data):
        """Override create to manually set item_id"""
        # Get the next available item_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(item_id) FROM inventory_items")
            max_id = cursor.fetchone()[0]
            next_id = (max_id or 0) + 1
        
        # Set the item_id
        validated_data['item_id'] = next_id
        
        # Create the instance
        instance = InventoryItem(**validated_data)
        instance.save()
        return instance
    
    class Meta:
        model = InventoryItem
        fields = ['item_id', 'item_name', 'category', 'quantity_available', 
                  'reorder_level', 'supplier', 'unit_price', 'expiry_date',
                  'is_low_stock', 'created_at', 'updated_at', 'admin_id']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


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
