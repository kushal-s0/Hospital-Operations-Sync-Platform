from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InventoryCategoryViewSet, 
    InventoryItemViewSet, 
    InventoryTransactionViewSet,
    get_stock_prediction,
    get_all_inventory_alerts,
    get_disease_demand_forecast,
    get_weather_based_prediction,
    manual_prediction
)

router = DefaultRouter()
router.register(r'categories', InventoryCategoryViewSet)
router.register(r'items', InventoryItemViewSet)
router.register(r'transactions', InventoryTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # ML Prediction Endpoints (AUTOMATIC - data from database)
    path('predict/<int:item_id>/', get_stock_prediction, name='stock-prediction'),
    path('alerts/', get_all_inventory_alerts, name='inventory-alerts'),
    path('demand-forecast/', get_disease_demand_forecast, name='demand-forecast'),
    path('weather-prediction/', get_weather_based_prediction, name='weather-prediction'),
    
    # Manual prediction (for testing)
    path('predict/manual/', manual_prediction, name='manual-prediction'),
]
