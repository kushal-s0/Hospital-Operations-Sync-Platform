from django.urls import path
from .views import CityDashboardAPIView

urlpatterns = [
    path('city-dashboard/', CityDashboardAPIView.as_view(), name='city-dashboard'),
]
