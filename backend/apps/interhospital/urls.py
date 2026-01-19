from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, CapacitySnapshotViewSet, CityDashboardAPIView

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'capacity', CapacitySnapshotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('city-dashboard/', CityDashboardAPIView.as_view(), name='city-dashboard'),
]
