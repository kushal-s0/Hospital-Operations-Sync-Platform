from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OPDQueueViewSet, OPDStatisticsViewSet

router = DefaultRouter()
router.register(r'queue', OPDQueueViewSet, basename='opd-queue')
router.register(r'statistics', OPDStatisticsViewSet, basename='opd-statistics')

urlpatterns = [
    path('', include(router.urls)),
]
