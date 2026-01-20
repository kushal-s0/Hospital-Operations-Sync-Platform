from django.urls import path
from .views import CityDashboardAPIView
from .views import CityDashboardAPIView, HospitalListAPIView

urlpatterns = [
    path('hospitals/', HospitalListAPIView.as_view(), name='hospitals-list'),
    path('city-dashboard/', CityDashboardAPIView.as_view(), name='city-dashboard'),
]
