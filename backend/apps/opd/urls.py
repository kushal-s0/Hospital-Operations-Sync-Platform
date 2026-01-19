from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OPDQueueViewSet, OPDStatisticsViewSet

router = DefaultRouter()
router.register(r'queue', OPDQueueViewSet)
router.register(r'statistics', OPDStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
