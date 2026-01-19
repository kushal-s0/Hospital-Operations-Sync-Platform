from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from apps.authentication.models import InventoryItem
from .models import InventoryCategory, InventoryTransaction
from .serializers import (
    InventoryCategorySerializer, 
    InventoryItemSerializer, 
    InventoryTransactionSerializer
)


class InventoryCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for InventoryCategory CRUD operations."""
    
    queryset = InventoryCategory.objects.all()
    serializer_class = InventoryCategorySerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    """ViewSet for InventoryItem CRUD operations."""
    
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock."""
        low_stock_items = InventoryItem.objects.filter(
            quantity_available__lte=models.F('reorder_level')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for InventoryTransaction CRUD operations."""
    
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
