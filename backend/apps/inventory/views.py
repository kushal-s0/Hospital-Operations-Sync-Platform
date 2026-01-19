from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import InventoryCategory, InventoryItem, InventoryTransaction
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
            current_stock__lte=models.F('minimum_stock')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get items expiring within 30 days."""
        from django.utils import timezone
        from datetime import timedelta
        
        threshold_date = timezone.now().date() + timedelta(days=30)
        expiring_items = InventoryItem.objects.filter(
            expiry_date__lte=threshold_date,
            expiry_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(expiring_items, many=True)
        return Response(serializer.data)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for InventoryTransaction CRUD operations."""
    
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer
