from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReceptionistDashboardViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'dashboard', ReceptionistDashboardViewSet, basename='receptionist-dashboard')
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
]
