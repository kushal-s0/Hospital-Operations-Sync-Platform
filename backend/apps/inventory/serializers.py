from rest_framework import serializers
from .models import InventoryCategory, InventoryItem, InventoryTransaction


class InventoryCategorySerializer(serializers.ModelSerializer):
    """Serializer for InventoryCategory model."""
    
    class Meta:
        model = InventoryCategory
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for InventoryItem model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventoryTransactionSerializer(serializers.ModelSerializer):
    """Serializer for InventoryTransaction model."""
    
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = '__all__'
