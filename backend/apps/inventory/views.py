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


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for predictions
def get_weather_based_prediction(request):
    """
    Get medicine demand prediction based on weather and AQI conditions.
    
    AUTOMATIC - Fetches real-time weather and AQI data.
    Uses rule-based predictions to forecast disease spikes.
    
    Response:
    {
        "weather_aqi_factors": [
            {
                "trigger": "High Air Pollution",
                "value": "AQI: 175 (Unhealthy)",
                "diseases": ["Respiratory Infection", "Asthma"],
                "severity": "High",
                "recommendation": "Stock up on respiratory medicines"
            }
        ],
        "disease_impact": {...},
        "predicted_medicine_demand": {
            "Salbutamol Inhaler": {
                "quantity": 45,
                "base_quantity": 30,
                "related_diseases": ["Asthma"],
                "urgency": "High"
            }
        },
        "current_weather": {
            "temperature": 32.5,
            "humidity": 75,
            "description": "light rain"
        },
        "current_aqi": {
            "aqi": 175,
            "quality": "Unhealthy"
        }
    }
    """
    try:
        from .weather_predictor import get_weather_predictor
        
        # Get predictor instance
        predictor = get_weather_predictor()
        
        # Get weather-based predictions
        prediction = predictor.predict_medicine_demand()
        
        # Add current conditions
        conditions = predictor.get_current_conditions()
        prediction['current_weather'] = conditions['weather']
        prediction['current_aqi'] = conditions['aqi']
        prediction['location'] = conditions['location']
        
        return Response(prediction)
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
    
    def list(self, request, *args, **kwargs):
        """Get all inventory items with pagination and sorting by expiry date."""
        queryset = self.get_queryset()
        
        # Sort by expiry date if available (items without expiry go last)
        # Since expiry_date doesn't exist in current schema, we'll order by item_name for now
        queryset = queryset.order_by('item_name')
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_stock(self, request):
        """Add new inventory item."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': str(e), 'details': 'Failed to add inventory item'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['patch'])
    def update_stock(self, request, pk=None):
        """Update stock quantity for existing item."""
        try:
            item = self.get_object()
            stock_to_add = int(request.data.get('stock_quantity', 0))
            
            if stock_to_add > 0:
                item.quantity_available = (item.quantity_available or 0) + stock_to_add
                item.save()
                
                serializer = self.get_serializer(item)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'stock_quantity must be positive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid stock_quantity'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock."""
        low_stock_items = InventoryItem.objects.filter(
            quantity_available__lte=models.F('reorder_level')
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
