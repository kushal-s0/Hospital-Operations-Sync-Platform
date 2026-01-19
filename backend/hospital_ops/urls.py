"""
URL configuration for hospital_ops project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/patients/', include('apps.patients.urls')),
    path('api/beds/', include('apps.beds.urls')),
    path('api/opd/', include('apps.opd.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/admissions/', include('apps.admissions.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/interhospital/', include('apps.interhospital.urls')),
]
