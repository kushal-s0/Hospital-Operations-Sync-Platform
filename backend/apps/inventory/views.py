from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import models
from .models import InventoryCategory, InventoryItem, InventoryTransaction
from .serializers import (
    InventoryCategorySerializer, 
    InventoryItemSerializer, 
    InventoryTransactionSerializer
)


# =============================================================================
# ML PREDICTION API ENDPOINTS
# =============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for predictions
def get_stock_prediction(request, item_id):
    """
    Get unified stock prediction for a specific item.
    
    AUTOMATIC - No manual input needed!
    Data is pulled from database automatically.
    
    Response:
    {
        "item": {"id": 1, "name": "Paracetamol", "current_stock": 100},
        "usage_based_prediction": {"days_until_stockout": 5.2, "probability": 0.85},
        "disease_based_prediction": {"expected_demand_this_week": 150},
        "combined_analysis": {"risk_score": 0.72, "urgency": "HIGH", "recommendation": "..."}
    }
    """
    try:
        from .ml_predictor import get_predictor
        predictor = get_predictor()
        result = predictor.get_unified_prediction(item_id=item_id)
        return Response(result)
    except InventoryItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for predictions
def get_all_inventory_alerts(request):
    """
    Get alerts for ALL inventory items.
    
    AUTOMATIC - Scans entire inventory and returns items needing attention.
    No manual input required!
    
    Response:
    {
        "total_items_scanned": 100,
        "items_needing_attention": 15,
        "high_priority": 5,
        "medium_priority": 10,
        "alerts": [...]
    }
    """
    try:
        from .ml_predictor import get_predictor
        predictor = get_predictor()
        result = predictor.get_all_alerts()
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for predictions
def get_disease_demand_forecast(request):
    """
    Get medicine demand forecast based on current patient admissions.
    
    AUTOMATIC - Pulls admission data from database.
    
    Optional query params:
    - days: Look back period for admissions (default: 7)
    
    Response:
    {
        "current_admissions": {"Respiratory Infection": 25, "Fever": 18},
        "total_patients": 73,
        "predicted_demand": {"Paracetamol 500mg": 625, "Azithromycin": 150}
    }
    """
    try:
        from .ml_predictor import get_predictor
        days = int(request.query_params.get('days', 7))
        predictor = get_predictor()
        result = predictor.predict_disease_demand()
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public access for predictions
def manual_prediction(request):
    """
    Manual prediction endpoint (for testing or override).
    
    Use this when you want to test with specific values
    instead of pulling from database.
    
    Request body:
    {
        "item_data": {
            "quantity_available": 50,
            "reorder_level": 100,
            "avg_daily_usage": 15,
            "usage_std": 5,
            "max_daily_usage": 25,
            "usage_last_7_days": 120,
            "usage_trend": 10,
            "category": "Medicine",
            "lead_time_days": 5
        }
    }
    """
    try:
        from .ml_predictor import get_predictor
        predictor = get_predictor()
        item_data = request.data.get('item_data')
        
        if not item_data:
            return Response({'error': 'item_data required'}, status=status.HTTP_400_BAD_REQUEST)
        
        result = predictor.predict_stock_depletion(item_data=item_data)
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
