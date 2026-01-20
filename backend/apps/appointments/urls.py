from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, book_appointment, get_available_doctors, get_departments

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('book/', book_appointment, name='book-appointment'),
    path('doctors/', get_available_doctors, name='available-doctors'),
    path('departments/', get_departments, name='departments'),
]
