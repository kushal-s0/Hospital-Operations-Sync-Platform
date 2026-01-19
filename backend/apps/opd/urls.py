from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OPDQueueViewSet, OPDStatisticsViewSet, predict_wait_time

router = DefaultRouter()
router.register(r'queue', OPDQueueViewSet)
router.register(r'statistics', OPDStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # ML Wait Time Prediction Endpoint
    path('predict-wait-time/', predict_wait_time, name='predict-wait-time'),
]
