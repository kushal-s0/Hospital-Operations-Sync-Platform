from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReceptionistDashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', ReceptionistDashboardViewSet, basename='receptionist-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
